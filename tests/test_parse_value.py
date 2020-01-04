import pytest

from config_file.parsers.parse_value import parse_value


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
    ],
)
def test_parse_value(test_input, expected):
    result = parse_value(test_input)
    assert result == expected
