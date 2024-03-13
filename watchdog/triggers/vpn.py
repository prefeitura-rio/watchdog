# -*- coding: utf-8 -*-
# flake8: noqa: E501
import concurrent.futures
import socket
import traceback
from typing import Any, Dict, List, Tuple

from watchdog.triggers.base import Trigger
from watchdog.utils import log


class VpnTrigger(Trigger):
    def __init__(
        self,
        ips_ports: List[Tuple[str, int, str]],
    ):
        """
        Initializes the late runs trigger.
        """
        self._ips_ports = ips_ports

    def _check_ip_port(self, ip: str, port: int, name: str) -> bool:
        """
        Checks whether a given IP and port is reachable.
        """
        try:
            with socket.create_connection((ip, port), timeout=5):
                log(f"VPN connection to {name} ({ip}:{port}) is OK")
                return True
        except:
            log(f"VPN connection to {name} ({ip}:{port}) has failed", "error")
            return False

    def trigger(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks whether this has been triggered.

        Information here follows the format:

        ```py
        {
            "failed": [
                (ip, port, name),
            ]
        }
        ```
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(
                lambda ip_port: self._check_ip_port(*ip_port), self._ips_ports
            )
        failed = [
            ip_port for ip_port, result in zip(self._ips_ports, results) if not result
        ]
        return len(failed) > 0, {"failed": failed}

    @classmethod
    def to_message(cls, info: Dict[str, Any]) -> str:
        """
        Converts the information to a message. Useful for messaging handlers.
        """
        try:
            message = "🚨 Alerta de falha de conexão 🚨\n\n"
            for ip, port, name in info["failed"]:
                message += f"❌ {name} -> {ip}:{port}\n"
        except:  # noqa: E722
            print(traceback.format_exc())
            message = "🚨 Falha ao formar mensagem de falha de conexão 🚨"
        return message
