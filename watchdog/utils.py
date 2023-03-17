# -*- coding: utf-8 -*-
from typing import List

from loguru import logger

###
#
# Text utilities
#
###


def log(message: str, level: str = "info") -> None:
    """
    Logs a message to stdout.
    """
    LOG_FUNCTIONS = {
        "info": logger.info,
        "debug": logger.debug,
        "warning": logger.warning,
        "error": logger.error,
        "critical": logger.critical,
    }
    LOG_FUNCTIONS[level](message)


def smart_split(
    text: str,
    max_length: int,
    separator: str = " ",
) -> List[str]:
    """
    Splits a string into a list of strings.
    """
    if len(text) <= max_length:
        return [text]

    separator_index = text.rfind(separator, 0, max_length)
    if (separator_index >= max_length) or (separator_index == -1):
        raise ValueError(
            f'Cannot split text "{text}" into {max_length}'
            f'characters using separator "{separator}"'
        )

    return [
        text[:separator_index],
        *smart_split(
            text[separator_index + len(separator) :],  # noqa: E203
            max_length,
            separator,
        ),
    ]


def to_human_readable_time(seconds: float) -> str:
    """
    Converts a number of seconds to a human readable time.
    """
    total_seconds: int = round(seconds)
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if days:
        message = f"{days}d {hours}h {minutes}m {seconds}s"
    elif hours:
        message = f"{hours}h {minutes}m {seconds}s"
    elif minutes:
        message = f"{minutes}m {seconds}s"
    else:
        message = f"{seconds}s"
    return message
