"""
This module allows you to parse a string into its native type.

Example:
    parse_value('5') -> 5   (int)
    parse_value('-5') -> -5 (int)

    parse_value('5.52') -> 5.52   (float)
    parse_value('-53.2') -> -53.2 (float)

    parse_value('blahfafda') -> 'blahfafda' (string)

    parse_value('true') -> True (bool)
    parse_value('FALSE') -> False (bool)


"5".isdigit() -> True
"-5".isdigit() -> False
can_be_parsed_as_int("-5") -> True
parse_value("-5") -> -5
"""
import ast
import re
from distutils.util import strtobool
from typing import Any


def parse_value(value: Any) -> Any:
    """Parse a value into native type.

    Args:
        value: The value to parse.

    Returns:
        The parsed value, if it could be parsed
        as a dictionary, list, int, float, or bool.
        Otherwise, it simply returns the original
        passed in value.
    """
    if isinstance(value, dict):
        parsed = {}

        for item in value:
            parsed[item] = parse_value(value[item])

        return parsed

    if isinstance(value, list):
        parsed = []

        for item in value:
            parsed.append(parse_value(item))

        return parsed

    if can_be_parsed_as_int(value):
        return int(value.strip()) if isinstance(value, str) else int(value)

    if can_be_parsed_as_float(value):
        return float(value.strip()) if isinstance(value, str) else float(value)

    if can_be_parsed_as_bool(value):
        return bool(value) if isinstance(value, bool) else bool(strtobool(value))

    if can_be_parsed_as_dict(value):
        return parse_value(ast.literal_eval(value.strip()))

    if can_be_parsed_as_list(value):
        return parse_value(ast.literal_eval(value.strip()))

    return value


def can_be_parsed_as_int(value: Any) -> bool:
    """Check whether a value can be parsed as a integer.

    Args:
        value: The value to check if it can be parsed as an integer.

    Returns:
        True if we can parse the value as a integer. False otherwise.
    """
    if isinstance(value, int) and not type(value) is bool:
        return True

    if not isinstance(value, str):
        return False

    value = value.strip()

    if value.startswith("-"):
        return value[1:].isdigit()

    return value.isdigit()


def can_be_parsed_as_float(value: Any) -> bool:
    FLOAT_REGEX = r"^\d*\.\d+$"

    if isinstance(value, float):
        return True

    if not isinstance(value, str):
        return False

    value = value.strip()

    if value.startswith("-"):
        value = value[1:]

    return bool(re.match(FLOAT_REGEX, value))


def can_be_parsed_as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return True

    if not isinstance(value, str):
        return False

    value = value.lower().strip()

    return value == "true" or value == "false"


def can_be_parsed_as_dict(value: Any) -> bool:
    if isinstance(value, dict):
        return True

    if not isinstance(value, str):
        return False

    value = value.strip()

    if value[0] == "{" and value[-1] == "}":
        try:
            ast.literal_eval(value)
            return True
        except Exception:
            return False

    return False


def can_be_parsed_as_list(value) -> bool:
    if isinstance(value, list):
        return True

    if not isinstance(value, str):
        return False

    value = value.strip()

    if value[0] == "[" and value[-1] == "]":
        try:
            ast.literal_eval(value)
            return True
        except Exception:
            return False

    return False
