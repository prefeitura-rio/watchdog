# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

from prefect import Client

from watchdog.triggers.base import Trigger
from watchdog.utils import to_human_readable_time


class PrefectAgents(Trigger):
    def __init__(self, last_queried_delay: timedelta = None):
        """
        Initializes the Prefect Agents trigger.
        """
        if last_queried_delay is None:
            last_queried_delay = timedelta(minutes=5)
        self._last_queried_delay = last_queried_delay

    def _get_client(self) -> Client:
        """
        Returns a Prefect API client.
        """
        return Client()

    def _query_agents(self) -> Dict[str, Dict[str, Any]]:
        """
        Queries the Prefect API for all agents and returns them and
        whether they are alive or not.

        Args:
            last_queried_delay (timedelta): The time since the last query.

        Returns:
            Dict[str, Dict[str, Any]]: The information for this trigger. Follows the format:

            ```py
            {
                "api": {
                    "alive": True,
                },
                "agents": {
                    "agent_name": {
                        "alive": True,
                        "last_queried": timedelta(total_seconds=60),
                    },
                    ...
                }
            }
        """
        api_alive: bool = True
        agents: List[Dict[str, Any]] = None
        try:
            client: Client = self._get_client()
            now: datetime = None
            response = client.graphql(
                {
                    "query": {
                        "agent": {
                            "labels",
                            "last_queried",
                        }
                    }
                }
            )
            agents = response["data"]["agent"]
        except Exception:
            api_alive = False
            agents = []
        # Each agent is a dictionary with the following format:
        # {
        #     "labels": [
        #         "your-agent-name",
        #     ],
        #     "last_queried": "2020-01-01T00:00:00.000+00:00",
        # }
        # Order the agents by name.
        agents = sorted(agents, key=lambda agent: agent["labels"][0])
        agents_info: Dict[str, Dict[str, Any]] = {
            "api": {
                "alive": api_alive,
            },
            "agents": {},
        }
        for agent in agents:
            agent_name: str = agent["labels"][0]
            last_queried: datetime = datetime.strptime(
                agent["last_queried"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
            if not now:
                now = datetime.now(tz=last_queried.tzinfo)
            agents_info["agents"][agent_name] = {
                "alive": last_queried + self._last_queried_delay > now,
                "last_queried": now - last_queried,
            }
        return agents_info

    def trigger(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks whether this has been triggered.

        Information here follows the format:

        ```py
        {
            "api": {
                "alive": True,
            },
            "agents": {
                "agent_name": {
                    "alive": True,
                    "last_queried": timedelta(total_seconds=60),
                },
                ...
            }
        }
        ```
        """
        info = self._query_agents()
        any_agent_dead: bool = False
        api_dead: bool = not info["api"]["alive"]
        return any_agent_dead or api_dead, info

    @classmethod
    def to_message(cls, info: Dict[str, Any]) -> str:
        """
        Converts the information to a message. Useful for messaging handlers.
        """
        api_status: bool = info["api"]["alive"]
        message: str = ">>> Prefect <<<\n\nAPI: "
        if api_status:
            message += "🟢"
        else:
            message += "🔴"
        if len(list(info["agents"].keys())):
            message += "\n\nAgents:"
            for agent_name, agent_info in info["agents"].items():
                agent_status: bool = agent_info["alive"]
                message += f"\n\n- {agent_name:<17} "
                if agent_status:
                    message += "🟢"
                else:
                    message += "🔴"
                message += "\n  last query "
                message += to_human_readable_time(
                    agent_info["last_queried"].total_seconds()
                )
                message += " ago"
        message = message.replace(">", "\\>")
        message = message.replace("<", "\\<")
        message = message.replace("-", "\\-")
        message = message.replace("=", "\\=")
        return message
