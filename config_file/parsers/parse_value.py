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


def parse_value(value):
    if type(value) is dict:
        parsed = {}

        for item in value:
            parsed[item] = parse_value(value[item])

        return parsed

    if type(value) is list:
        parsed = []

        for item in value:
            parsed.append(parse_value(item))

        return parsed

    if can_be_parsed_as_int(value):
        return int(value)

    if can_be_parsed_as_float(value):
        return float(value)

    if can_be_parsed_as_bool(value):
        return value if type(value) is bool else bool(strtobool(value))

    if can_be_parsed_as_dict(value):
        return parse_value(ast.literal_eval(value))

    if can_be_parsed_as_list(value):
        return parse_value(ast.literal_eval(value))

    return value


def can_be_parsed_as_int(value) -> bool:
    if type(value) is int:
        return True

    if type(value) is not str:
        return False

    if value.startswith("-"):
        return value[1:].isdigit()

    return value.isdigit()


def can_be_parsed_as_float(value) -> bool:
    FLOAT_REGEX = r"^\d*\.\d+$"

    if type(value) is float:
        return True

    if type(value) is not str:
        return False

    if value.startswith("-"):
        value = value[1:]

    return bool(re.match(FLOAT_REGEX, value))


def can_be_parsed_as_bool(value) -> bool:
    if type(value) is bool:
        return True

    if type(value) is not str:
        return False

    return value.lower() == "true" or value.lower() == "false"


def can_be_parsed_as_dict(value) -> bool:
    if type(value) is dict:
        return True

    if type(value) is not str:
        return False

    value = value.strip()
    if value[0] == "{" and value[-1] == "}":
        try:
            ast.literal_eval(value)
            return True
        except SyntaxError:
            return False

    return False


def can_be_parsed_as_list(value) -> bool:
    if type(value) is dict:
        return True

    if type(value) is not str:
        return False

    value = value.strip()
    if value[0] == "[" and value[-1] == "]":
        try:
            ast.literal_eval(value)
            return True
        except SyntaxError:
            return False

    return False
