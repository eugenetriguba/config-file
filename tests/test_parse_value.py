import pytest

from config_file.parsers.parse_value import can_be_parsed_as_bool, parse_value


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("5", 5),
        ("-5", -5),
        ("-234.5", -234.5),
        ("35.5", 35.5),
        ("TRUE", True),
        ("true", True),
        ("false", False),
        ("blah", "blah"),
        (343, 343),
        (3.2, 3.2),
        (True, True),
        ({"blah": "5"}, {"blah": 5}),
        (
            {"blah": {"blah2": {"blah3": "false"}, "abc": "5.25", "boo": "tRuE"}},
            {"blah": {"blah2": {"blah3": False}, "abc": 5.25, "boo": True}},
        ),
        (
            ["5", "4.4", "faLSe", "trUE", "foo", "-5", "-5.2"],
            [5, 4.4, False, True, "foo", -5, -5.2],
        ),
    ],
)
def test_parse_value(test_input, expected):
    assert parse_value(test_input) == expected


def test_can_be_parsed_as_bool():
    """
    This is the section not being covered in the parse_value.py
    file from test_parse_value, but I don't think it's reachable
    from using it.
    """
    assert can_be_parsed_as_bool(5) is False
