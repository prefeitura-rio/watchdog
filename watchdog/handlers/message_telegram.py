# -*- coding: utf-8 -*-
from typing import Any, Dict

import telegram

from watchdog.handlers.base import Handler
from watchdog.triggers.base import Trigger
from watchdog.utils import smart_split


class MessageTelegram(Handler):
    def __init__(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id

    def _escape_markdown(self, text: str) -> str:
        return (
            text.replace("_", r"\_")
            .replace("*", r"\*")
            .replace("[", r"\[")
            .replace("`", r"\`")
            .replace("(", r"\(")
            .replace("-", r"\-")
            .replace(".", r"\.")
        )

    def handle(self, info: Dict[str, Any], trigger_class: Trigger = None) -> None:
        raw_message = self._escape_markdown(trigger_class.to_message(info))
        messages = smart_split(raw_message, 4096)
        bot = telegram.Bot(token=self._token)
        for message in messages:
            bot.send_message(
                chat_id=self._chat_id,
                text=message,
                parse_mode=telegram.ParseMode.MARKDOWN_V2,
            )
