import json

import pytest

from config_file.parsers.json_parser import JsonParser

test_json = {
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup "
                        + "languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"],
                    },
                    "GlossSee": "markup",
                }
            },
        },
    }
}


@pytest.mark.parametrize(
    "test_input,expected_result",
    [
        ("glossary", True),
        ("title", True),
        ("example glossary", False),
        ("GlossDiv", True),
        ("title", True),
        ("S", False),
        ("GlossList", True),
        ("GlossEntry", True),
        ("ID", True),
        ("SGML", False),
        ("GlossTerm", True),
        ("Standard Generalized Markup Language", False),
        ("Acronym", True),
        ("ISO 8879:1986", False),
        ("GlossDef", True),
        ("para", True),
        (
            "A meta-markup language, used to create markup languages such as DocBook.",
            False,
        ),
        ("GlossSeeAlso", True),
        ("GML", False),
        ("XML", False),
        ("GlossSee", True),
        ("markup", False),
    ],
)
def test_that_json_parser_can_find_keys(test_input, expected_result):
    parser = JsonParser(json.dumps(test_json))
    assert parser.has(test_input) == expected_result
