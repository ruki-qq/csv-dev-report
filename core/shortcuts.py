from typing import Any

from .logger import log


@log
def is_numeric(value: Any) -> bool:
    """
    Checking if value is numeric.

    Returns:
        True if the value is numeric, False otherwise.
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


@log
def convert_to_number(value: Any) -> int | float:
    """
    Converting value into numeric.

    Returns:
        Numeric value (int or float).

    Raises:
        ValueError: If value cannot be converted.
    """

    try:
        if "." in value:
            result = float(value)
            return result
        else:
            result = int(value)
            return result
    except ValueError:
        error_msg = f"Cannot convert value {value} to numeric."
        raise ValueError(error_msg)
