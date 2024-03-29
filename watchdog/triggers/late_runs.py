# -*- coding: utf-8 -*-
# flake8: noqa: E501
from datetime import timedelta
import json
import traceback
from typing import Any, Dict, Tuple

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry

from watchdog.triggers.base import Trigger
from watchdog.utils import to_human_readable_time


class LateRunsTrigger(Trigger):
    def __init__(
        self,
        prefect_api_url: str,
        prefect_api_auth_token: str,
        time_tolerance: timedelta = timedelta(minutes=5),
    ):
        """
        Initializes the late runs trigger.
        """
        self._prefect_api_url = prefect_api_url
        self._prefect_api_auth_token = prefect_api_auth_token
        self._time_tolerance = time_tolerance
        self._requests_session = requests.Session()
        self._requests_retries = Retry(
            total=5, backoff_factor=1, status_forcelist=[502, 503, 504]
        )
        self._requests_session.mount(
            "http://", HTTPAdapter(max_retries=self._requests_retries)
        )
        self._requests_session.mount(
            "https://", HTTPAdapter(max_retries=self._requests_retries)
        )

    def _graphql_query(self, query, variables: dict = None):
        """
        Perform a GraphQL query and return results.
        """
        variables = variables or {}
        headers = {
            "Authorization": f"Bearer {self._prefect_api_auth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        r = self._requests_session.post(
            self._prefect_api_url,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        return r.json()

    def _query_late_runs(self) -> pd.DataFrame:
        """
        Queries all late runs from the Prefect API and returns them.
        """
        query = """
            query UpcomingFlowRuns($projectId: uuid) {
                flow_run(
                    where: {flow: {project_id: {_eq: $projectId}}, state: {_in: ["Scheduled", "Queued"]}}
                    order_by: [{scheduled_start_time: asc}, {flow: {name: asc}}]
                ) {
                    id
                    name
                    state
                    labels
                    scheduled_start_time
                    version
                    flow {
                    id
                    name
                    }
                    __typename
                }
            }
        """
        data: dict = self._graphql_query(query=query)
        now = pd.Timestamp("today", tz="UTC")
        df = pd.json_normalize(data.get("data").get("flow_run"), sep="_")
        df["scheduled_start_time"] = pd.to_datetime(df["scheduled_start_time"])
        df["amount_late"] = (
            (now) - (df["scheduled_start_time"] + self._time_tolerance)
        ).dt.total_seconds()
        df_late = df[df["amount_late"] > 0]
        return df_late

    def trigger(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks whether this has been triggered.

        Information here follows the format:

        ```py
        {
            "records": [
                {
                    "flow_name": str,
                    "count": int
                }
            ]
        }
        ```
        """
        try:
            df = self._query_late_runs()
            trigger = len(df) > 0
            df_grouped = (
                df.groupby("flow_name")
                .agg({"id": "count", "amount_late": "max"})
                .reset_index()
            )
            df_grouped["count"] = df_grouped["id"]
            df_grouped.drop(columns=["id"], inplace=True)
            df_grouped.sort_values(by="amount_late", ascending=False, inplace=True)
            return trigger, {
                "records": json.loads(df_grouped.to_json(orient="records"))
            }
        except:  # noqa: E722
            print(traceback.format_exc())
            return True, {"error": True}

    @classmethod
    def to_message(cls, info: Dict[str, Any]) -> str:
        """
        Converts the information to a message. Useful for messaging handlers.
        """
        message = ""
        if "error" in info:
            message = "🚨 Falha ao consultar runs atrasadas 🚨"
        try:
            if "records" in info and len(info["records"]):
                message = "🚨 Alerta de runs atrasadas 🚨\n\n"
                for record in info["records"]:
                    message += f"- `{str(record['count']):<3}x {record['flow_name'][:60]:<60} (atraso máx: {to_human_readable_time(record['amount_late'])})`\n"
        except:  # noqa: E722
            print(traceback.format_exc())
            message = "🚨 Falha ao formar mensagem de runs atrasadas 🚨"
        return message
