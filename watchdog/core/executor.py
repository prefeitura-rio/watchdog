# -*- coding: utf-8 -*-
from typing import List

from namesgenerator import get_random_name

from watchdog.handlers.base import Handler
from watchdog.triggers.base import Trigger
from watchdog.utils import log


class Executor:
    def __init__(
        self, trigger: Trigger, handlers: List[Handler], friendly_name: str = None
    ):
        self._trigger = trigger
        self._handlers = handlers
        self._friendly_name = friendly_name or get_random_name()
        log(f"Starting executor {self._friendly_name} with:")
        log(" * Trigger: {}".format(trigger.__class__.__name__))
        log(" * Handlers: {}".format([h.__class__.__name__ for h in handlers]))

    def run(self):
        log(f"Executor {self._friendly_name} running")
        trigger, info = self._trigger.trigger()
        log("- Trigger: {}".format(trigger))
        if trigger:
            for handler in self._handlers:
                log("- Calling handler {}".format(handler.__class__.__name__))
                handler.handle(info, self._trigger.__class__)
