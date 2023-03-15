# -*- coding: utf-8 -*-
from os import getenv


def getenv_notnull(key: str) -> str:
    """
    Gets an environment variable and raises an error if it is null.
    """
    value = getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is null. Please set it.")
    return value


class Settings:
    __slots__ = ()

    # Discord settings
    DISCORD_WEBHOOK_URL = getenv_notnull("DISCORD_WEBHOOK_URL")

    # Telegram settings
    TELEGRAM_CHAT_ID = getenv_notnull("TELEGRAM_CHAT_ID")
    TELEGRAM_TOKEN = getenv_notnull("TELEGRAM_TOKEN")

    # Prefect API settings
    PREFECT_API_URL = getenv_notnull("PREFECT_API_URL")
    PREFECT_API_AUTH_TOKEN = getenv_notnull("PREFECT_API_AUTH_TOKEN")


settings = Settings()
