# -*- coding: utf-8 -*-
from typing import Any, Dict

import requests

from watchdog.handlers.base import Handler
from watchdog.triggers.base import Trigger
from watchdog.utils import smart_split


class MessageDiscord(Handler):
    def __init__(self, webhook_url: str):
        self._webhook_url = webhook_url

    def handle(self, info: Dict[str, Any], trigger_class: Trigger = None) -> None:
        raw_message = trigger_class.to_message(info)
        messages = smart_split(raw_message, 4096)
        for message in messages:
            requests.post(self._webhook_url, data={"content": message})
