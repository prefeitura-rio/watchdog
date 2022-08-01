# -*- coding: utf-8 -*-
from typing import List


###
#
# Text utilities
#
###
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
    seconds: int = round(seconds)
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 60 * 60:
        return f"{seconds // 60} minutes"
    elif seconds < 60 * 60 * 24:
        return f"{seconds // 3600} hours"
    else:
        return f"{seconds // 86400} days"
