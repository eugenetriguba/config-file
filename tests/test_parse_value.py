from datetime import datetime

import pytest

from config_file.parse_value import (
    can_be_parsed_as_bool,
    can_be_parsed_as_dict,
    can_be_parsed_as_float,
    can_be_parsed_as_int,
    can_be_parsed_as_list,
    parse_value,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("5", 5),
        ("-5", -5),
        ("0", 0),
        ("-234.5", -234.5),
        ("35.5", 35.5),
        ("TRUE", True),
        ("true", True),
        ("false", False),
    ],
)
def test_parse_value_parses_ints_floats_and_bools(test_input, expected):
    """
    config_file.parse_value.parse_value

    Parses string values that contain ints, floats, and booleans into
    their native representation.
    """
    assert parse_value(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"blah": "5"}, {"blah": 5}),
        (
            {"blah": {"blah2": {"blah3": "fAlSe"}, "abc": "5.25", "boo": "tRuE"}},
            {"blah": {"blah2": {"blah3": False}, "abc": 5.25, "boo": True}},
        ),
        ("{ 'key': '5', 'key2': 'fAlSE' }", {"key": 5, "key2": False}),
        (
            ["5", "4.4", "faLSe", "trUE", "foo", "-5", "-5.2"],
            [5, 4.4, False, True, "foo", -5, -5.2],
        ),
        (" [1, 2, 3] ", [1, 2, 3]),
        ("  [True, [1, 5], {}, 5.5]", [True, [1, 5], {}, 5.5]),
        ("  [ [ [ [] ]] ]  ", [[[[]]]]),
    ],
)
def test_parse_value_parses_dicts_and_lists(test_input, expected):
    """
    config_file.parse_value.parse_value

    Parses string values that contain dictionaries or lists into
    their native representation.
    """
    assert parse_value(test_input) == expected


@pytest.mark.parametrize("test_input", ["blah", datetime(2020, 1, 1)])
def test_parse_value_returns_values_that_cannot_be_parsed(test_input):
    """
    config_file.parse_value.parse_value

    If a value is given that cannot be parsed by parse_value,
    it should simply return that value back.
    """
    assert parse_value(test_input) == test_input


@pytest.mark.parametrize(
    "test_input",
    [(343, 343), (3.2, 3.2), (True, True), (False, False), ({}, {}), ([], [])],
)
def test_parse_value_returns_values_that_are_already_in_their_native_type(test_input):
    """
    config_file.parse_value.parse_value

    Returns back the inputted value if it is already in its native type.
    """
    assert parse_value(test_input) == test_input


@pytest.mark.parametrize("value", [-1, 0, 1, "1", "-1", "   0   "])
def test_values_that_can_be_parsed_as_int(value):
    """
    config_file.parse_value.can_be_parsed_as_int

    Returns True for values that can be parsed as an int.
    """
    assert can_be_parsed_as_int(value)


@pytest.mark.parametrize(
    "value", [True, False, 5.5, "5.5", [], {}, "ruff", datetime.now()]
)
def test_values_that_cannot_be_parsed_as_int(value):
    """
    config_file.parse_value.can_be_parsed_as_int

    Returns False for values that cannot be parsed as an int.
    """
    assert not can_be_parsed_as_int(value)


@pytest.mark.parametrize("value", [5.5, -1.2, ".1", "5.5", "   1.1  ", "-0.0", "0.0"])
def test_values_that_can_be_parsed_as_float(value):
    """
    config_file.parse_value.can_be_parsed_as_float

    Returns True for values that can be parsed as an float.
    """
    assert can_be_parsed_as_float(value)


@pytest.mark.parametrize(
    "value",
    [
        545,
        0,
        -3,
        "1",
        "-1",
        True,
        False,
        "   0   ",
        "0..0",
        [],
        {},
        "ruff",
        datetime.now(),
    ],
)
def test_values_that_cannot_be_parsed_as_float(value):
    """
    config_file.parse_value.can_be_parsed_as_float

    Returns False for values that cannot be parsed as an float.
    """
    assert not can_be_parsed_as_float(value)


@pytest.mark.parametrize(
    "value", [True, False, "false", "true", "TRUE", "FALSE", "  FALSE  ", "  TRUE  "]
)
def test_values_that_can_be_parsed_as_bool(value):
    """
    config_file.parse_value.can_be_parsed_as_bool

    Returns True for values that can be parsed as a bool.
    """
    assert can_be_parsed_as_bool(value)


@pytest.mark.parametrize("value", [0, 1, -1, 5.3, "ruff", {}, [], datetime.now()])
def test_values_that_cannot_be_parsed_as_bool(value):
    """
    config_file.parse_value.can_be_parsed_as_bool

    Returns False for values that cannot be parsed as a bool.
    """
    assert not can_be_parsed_as_bool(value)


@pytest.mark.parametrize("value", [{}, {"hello": 5}, "{}", "  {  }  ", "{'test': 5}"])
def test_values_that_can_be_parsed_as_dict(value):
    """
    config_file.parse_value.can_be_parsed_as_dict

    Returns True for values that can be parsed as a dict.
    """
    assert can_be_parsed_as_dict(value)


@pytest.mark.parametrize("value", [0, 5, -1, 5.5, [], "ruff", " { invalid } "])
def test_values_that_cannot_be_parsed_as_dict(value):
    """
    config_file.parse_value.can_be_parsed_as_dict

    Returns False for values that cannot be parsed as a dict.
    """
    assert not can_be_parsed_as_dict(value)


@pytest.mark.parametrize("value", [[], [1, 2, True, 5.5], "[]", " [] ", " [1, 2, 3]"])
def test_values_that_can_be_parsed_as_list(value):
    """
    config_file.parse_value.can_be_parsed_as_list

    Returns True for values that can be parsed as a list.
    """
    assert can_be_parsed_as_list(value)


@pytest.mark.parametrize("value", [0, 5, -1, 5.5, {}, "ruff", " [ invalid ] "])
def test_values_that_cannot_be_parsed_as_list(value):
    """
    config_file.parse_value.can_be_parsed_as_list

    Returns False for values that cannot be parsed as a list.
    """
    assert not can_be_parsed_as_list(value)
