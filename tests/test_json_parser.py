import json

import pytest

from config_file.parsers.json_parser import JsonParser, ParsingError


@pytest.mark.parametrize("test_json", ["{'test': }", "[section]\nblah = value\n\n"])
def test_invalid_json(test_json):
    with pytest.raises(ParsingError):
        JsonParser(test_json)


def test_that_json_parser_can_stringify():
    json_str = '{"test": 5, "blah": true}'
    parser = JsonParser(json_str)
    assert parser.stringify() == json_str


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
    assert parser.get(section_key, parse_types=parse_type) == expected_result


@pytest.mark.parametrize(
    "key, value", [("zip", "zipzip"), ("foo.bar.foobar", 5), ("foo.baz", "bar")]
)
def test_that_json_parser_can_set_keys(key, value):
    test_json = {
        "foo": {
            "baz": 5,
            "boo": "4.4",
            "bar": {"test_key": "foobar", "foobar": {"test": True}},
        },
        "bar": {"baz": 10},
        "zip": "piz",
    }

    parser = JsonParser(json.dumps(test_json))
    parser.set(key, value)
    assert parser.get(key) == value


@pytest.mark.parametrize(
    "key, test_json, expected_json",
    [
        ("foo", {"foo": "bar", "baz": 5}, {"baz": 5}),
        ("foo.bar", {"foo": {"bar": 5}}, {"foo": {}}),
    ],
)
def test_that_json_parser_can_delete_keys(key, test_json, expected_json):
    parser = JsonParser(json.dumps(test_json))
    parser.delete(key)
    assert parser.stringify() == json.dumps(expected_json)


@pytest.mark.parametrize(
    "test_json, key, expected_output",
    [({"foo": {"bar": 5, "baz": {"bar": 10, "bam": {"bar": 15}}}}, "bar", [5, 10, 15])],
)
def test_that_json_parser_can_retrieve_all_keys(test_json, key, expected_output):
    parser = JsonParser(json.dumps(test_json))
    assert parser.get(key, retrieve_all=True) == expected_output


@pytest.mark.parametrize(
    "test_json, key, value, expected_output",
    [
        (
            {"foo": {"bar": 5, "baz": {"bar": 10, "bam": {"bar": 15}}}},
            "bar",
            "new_value",
            ["new_value", "new_value", "new_value"],
        )
    ],
)
def test_that_json_parser_can_set_all_keys(test_json, key, value, expected_output):
    parser = JsonParser(json.dumps(test_json))
    parser.set(key, value, set_all=True)
    assert parser.get(key, retrieve_all=True) == expected_output


@pytest.mark.parametrize(
    "test_json, key, expected_output",
    [
        (
            {"foo": {"bar": 5, "baz": {"bar": 10, "bam": {"bar": 15}}}},
            "bar",
            {"foo": {"baz": {"bam": {}}}},
        )
    ],
)
def test_that_json_parser_can_delete_all_keys(test_json, key, expected_output):
    parser = JsonParser(json.dumps(test_json))
    parser.delete(key, delete_all=True)
    assert parser.stringify() == json.dumps(expected_output)
