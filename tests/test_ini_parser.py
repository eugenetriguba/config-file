import pytest

from config_file.exceptions import ParsingError, MissingKeyError
from config_file.parsers.ini_parser import IniParser


@pytest.mark.parametrize("ini_file", ["blahblahblah", "{ 'key1': 5 }"])
def test_incorrect_ini_formats(ini_file):
    with pytest.raises(ParsingError):
        IniParser(ini_file)


@pytest.mark.parametrize(
    "section_key,expected_value",
    [
        ("test_section.intkey", "5"),
        ("test_section.strkey", "blah"),
        ("test_section.boolkey", "false"),
        ("test_section.floatkey", "5.3"),
        (
            "test_section",
            {"intkey": "5", "strkey": "blah", "boolkey": "false", "floatkey": "5.3"},
        ),
    ],
)
def test_that_ini_parser_can_get_values(section_key, expected_value):
    ini_file = """[test_section]
intkey = 5
strkey = blah
boolkey = false
floatkey = 5.3

"""
    parser = IniParser(ini_file)
    assert parser.get(section_key) == expected_value


@pytest.mark.parametrize(
    "test_input", ["invalid.invalid_key"],
)
def test_that_getting_unknown_sections_or_keys_throws_errors(test_input):
    with pytest.raises(ParsingError):
        IniParser("").get(test_input)


@pytest.mark.parametrize(
    "section_key,value,expected_value",
    [
        ("test.key1", "different value", "[test]\nkey1 = different value\n\n"),
        ("test.key2", 5, "[test]\nkey1 = value1\nkey2 = 5\n\n"),
        ("test2.key", False, "[test]\nkey1 = value1\n\n[test2]\nkey = False\n\n"),
    ],
)
def test_that_ini_parser_can_set_values(section_key, value, expected_value):
    ini_file = """[test]\nkey1 = value1\n\n"""
    parser = IniParser(ini_file)
    parser.set(section_key, value)
    assert parser.stringify() == expected_value


@pytest.mark.parametrize(
    "ini_file",
    ["[test]\nkey1 = value1\n\n", "[test]\nblah = 5\n\n[section2]\nkey = 2\n\n", ""],
)
def test_that_ini_parser_can_be_stringified(ini_file):
    parser = IniParser(ini_file)
    assert parser.stringify() == ini_file


@pytest.mark.parametrize(
    "section_key,expected_result",
    [("test_section", ""), ("test_section.key1", "[test_section]\n\n")],
)
def test_that_ini_parser_can_delete(section_key, expected_result):
    ini_file = """[test_section]\nkey1 = value\n\n"""
    parser = IniParser(ini_file)
    parser.delete(section_key)
    assert parser.stringify() == expected_result


@pytest.mark.parametrize(
    "section_key", ["section_is_not_present", "test_section.but_key_is_not_present"],
)
def test_that_ini_parser_delete_raises_missing_key_errors(section_key):
    ini_file = """[test_section]\nkey1 = value\n\n"""
    parser = IniParser(ini_file)
    with pytest.raises(MissingKeyError):
        parser.delete(section_key)


@pytest.mark.parametrize(
    "section_key", ["test_section", "test_section.key1"],
)
def test_that_ini_parser_can_check_its_section_and_keys(section_key):
    ini_file = """[test_section]\nkey1 = value\n\n"""
    parser = IniParser(ini_file)
    assert parser.has(section_key)
