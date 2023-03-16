# -*- coding: utf-8 -*-
from time import sleep
import warnings

from apscheduler.schedulers.background import BackgroundScheduler

from watchdog.core import Executor
from watchdog.core.settings import settings
from watchdog.handlers import MessageDiscord

# from watchdog.handlers import MessageTelegram
from watchdog.triggers import LateRunsTrigger
from watchdog.utils import log

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

trigger_lateruns = LateRunsTrigger(
    prefect_api_url=settings.PREFECT_API_URL,
    prefect_api_auth_token=settings.PREFECT_API_AUTH_TOKEN,
)
handlers_lateruns = [
    MessageDiscord(webhook_url=settings.DISCORD_WEBHOOK_URL),
    # MessageTelegram(token=settings.TELEGRAM_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID),
]

executor = Executor(
    trigger=trigger_lateruns,
    handlers=handlers_lateruns,
    friendly_name="LateRuns",
)
scheduler: BackgroundScheduler = BackgroundScheduler()
scheduler.add_job(executor.run, "interval", minutes=1)

if __name__ == "__main__":
    scheduler.start()
    try:
        while True:
            sleep(5)
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
