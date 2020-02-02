import json

import pytest

from config_file.parsers.json_parser import JsonParser


@pytest.mark.parametrize(
    "test_input,expected_result",
    [
        ("glossary", True),
        ("title", True),
        ("example glossary", False),
        ("GlossDiv", True),
        ("title", True),
        ("5", False),
        ("GlossList", True),
        ("GlossEntry", True),
        ("ID", True),
        ("false", False),
        ("GlossTerm", True),
        ("Standard Generalized Markup Language", False),
        ("Acronym", True),
        ("ISO 8879:1986", False),
        ("GlossDef", True),
        ("para", True),
        (
            "A meta-markup language, used to create markup languages "
            "such as DocBook.",
            False,
        ),
        ("GlossSeeAlso", True),
        ("GML", False),
        ("XML", False),
        ("GlossSee", True),
        ("5.5", False),
    ],
)
def test_that_json_parser_can_find_keys(test_input, expected_result):
    test_json = {
        "glossary": {
            "title": "example glossary",
            "GlossDiv": {
                "title": "5",
                "GlossList": {
                    "GlossEntry": {
                        "ID": "false",
                        "SortAs": "SGML",
                        "GlossTerm": "Standard Generalized Markup Language",
                        "Acronym": "SGML",
                        "Abbrev": "ISO 8879:1986",
                        "GlossDef": {
                            "para": "A meta-markup language, used to create markup "
                            + "languages such as DocBook.",
                            "GlossSeeAlso": ["GML", "XML"],
                        },
                        "GlossSee": "5.5",
                    }
                },
            },
        }
    }

    parser = JsonParser(json.dumps(test_json))
    assert parser.has(test_input) == expected_result


@pytest.mark.parametrize(
    "test_json, section_key, parse_type, expected_result",
    [
        (
            {"glossary": {"title": "example glossary"}},
            "glossary.title",
            False,
            "example glossary",
        ),
        (
            {"glossary": {"title": "example glossary"}},
            "glossary.title",
            True,
            "example glossary",
        ),
        (
            {"glossary": {"title": "example glossary", "dict": {"blah": "5"}}},
            "glossary.dict",
            False,
            {"blah": "5"},
        ),
        (
            {"glossary": {"title": "example glossary", "dict": {"blah": "5"}}},
            "glossary.dict",
            True,
            {"blah": 5},
        ),
        (
            {
                "glossary": {
                    "title": "example glossary",
                    "dict": {"blah": "5", "second": {"third": "5"}},
                }
            },
            "glossary.dict",
            True,
            {"blah": 5, "second": {"third": 5}},
        ),
    ],
)
def test_that_json_parser_can_get_keys(
    test_json, section_key, parse_type, expected_result
):
    parser = JsonParser(json.dumps(test_json))
    assert parser.get(section_key, parse_type=parse_type) == expected_result


def test_that_json_parser_can_stringify():
    json_str = '{"test": 5, "blah": true}'
    parser = JsonParser(json_str)
    assert parser.stringify() == json_str
