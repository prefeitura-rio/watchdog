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

    # VPN settings
    VPN_IPS_PORTS = [
        ("10.39.64.50", 1433, "PIT/OCR"),
        ("10.70.6.64", 1521, "Processo.rio"),
        ("10.90.31.22", 1521, "SICOP"),
        ("10.2.221.127", 1433, "Divida ativa"),
        ("10.70.11.61", 1433, "SISCOR"),
        ("10.70.1.34", 1433, "1746 Replica"),
        ("10.70.6.103", 1433, "Gestao Escolar"),
        ("10.70.6.21", 1526, "Ergon (PROD)"),
        ("10.70.6.26", 1521, "Ergon COMLURB"),
        ("10.2.221.101", 1433, "EGPWEB (PROD)"),
        ("10.90.31.22", 1521, "SIGMA"),
    ]


settings = Settings()
