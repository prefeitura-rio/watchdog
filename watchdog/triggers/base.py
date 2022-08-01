# -*- coding: utf-8 -*-
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any, Dict, Tuple


class Trigger(ABC):
    @abstractmethod
    def trigger(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks whether this has been triggered.

        Returns:
            Tuple[bool, Dict[str, Any]]: A tuple of whether this has been triggered and all
                information needed for any handler.
        """

    @abstractclassmethod
    def to_message(cls, info: Dict[str, Any]) -> str:
        """
        Converts the information to a message. Useful for messaging handlers.

        Args:
            info (Dict[str, Any]): The information to convert.

        Returns:
            str: The message.
        """
