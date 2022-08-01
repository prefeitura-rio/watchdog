# -*- coding: utf-8 -*-
from os import getenv
import warnings

from apscheduler.schedulers.background import BackgroundScheduler

from watchdog.core import Executor
from watchdog.handlers import MessageDiscord
from watchdog.handlers import MessageTelegram
from watchdog.triggers import PrefectAgents
from watchdog.utils import log

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

trigger_prefect = PrefectAgents()
handlers_prefect = [
    MessageDiscord(webhook_url=getenv("DISCORD_WEBHOOK_URL")),
    MessageTelegram(token=getenv("TELEGRAM_TOKEN"), chat_id=getenv("TELEGRAM_CHAT_ID")),
]

executor = Executor(trigger=trigger_prefect, handlers=handlers_prefect)
scheduler = BackgroundScheduler()
scheduler.add_job(executor.run, "interval", minutes=1)

if __name__ == "__main__":
    scheduler.start()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        log("Scheduler stopped, reason=KeyboardInterrupt", "warning")
        pass
    except Exception as e:
        scheduler.shutdown()
        log("Scheduler stopped, reason=Exception", "warning")
        raise e
    finally:
        scheduler.shutdown()
        log("Scheduler stopped, reason=end of program", "warning")
        pass
    pass
