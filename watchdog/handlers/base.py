# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Dict

from watchdog.triggers.base import Trigger


class Handler(ABC):
    @abstractmethod
    def handle(self, info: Dict[str, Any], trigger_class: Trigger = None) -> None:
        """
        Handles the information when something triggers.
        """
