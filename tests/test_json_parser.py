import json

import pytest

from config_file.exceptions import ParsingError
from config_file.parsers.json_parser import JsonParser


def test_invalid_json(templated_parser):
    with pytest.raises(ParsingError):
        templated_parser("json", "invalid")


def test_that_json_parser_can_stringify(template_and_parser):
    template, parser = template_and_parser("json")

    assert parser.stringify() == template.read_text()


@pytest.mark.parametrize(
    "key",
    [
        "glossary",
        "title",
        "GlossDiv",
        "title",
        "GlossList",
        "GlossEntry",
        "ID",
        "GlossTerm",
        "Acronym",
        "GlossDef",
        "para",
        "GlossSeeAlso",
        "GlossSee",
    ],
)
def test_that_json_parser_can_find_wild_keys(key, templated_parser):
    parser = templated_parser("json", "glossary")
    assert parser.has(key, wild=True)


@pytest.mark.parametrize(
    "key",
    [
        "glossary",
        "glossary.title",
        "glossary.GlossDiv.GlossList.GlossEntry.GlossDef.para"
    ]
)
def test_that_json_parser_can_find_dot_keys(key, templated_parser):
    parser = templated_parser("json", "glossary")
    assert parser.has(key)


@pytest.mark.parametrize(
    "value",
    [
        "str_value",
        "5",
        "false",
        "Standard Generalized Markup Language",
        "ISO 8879:1986",
        "A meta-markup language, used to create markup languages such as DocBook.",
        "GML",
        "XML",
        "5.5",
    ],
)
def test_that_json_parser_does_not_find_values(value, templated_parser):
    parser = templated_parser("json", "glossary")
    assert not parser.has(value)


@pytest.mark.parametrize(
    "key, value",
    [
        ("glossary.title", "str_value"),
        ("glossary.dict", {"key": "str_value", "str_number": "5"}),
    ],
)
def test_that_json_parser_can_get_keys_without_parsing_types(
    templated_parser, key, value
):
    parser = templated_parser("json", "glossary")
    assert parser.get(key) == value


@pytest.mark.parametrize(
    "key, value", [("zip", "zipzip"), ("foo.bar.foobar", 5), ("foo.baz", "bar")]
)
def test_that_json_parser_can_set_keys(templated_parser, key, value):
    parser = templated_parser("json")

    parser.set(key, value)
    assert parser.get(key) == value


@pytest.mark.parametrize(
    "key",
    ["glossary", "glossary.dict_within_dict", "glossary.GlossDiv.GlossList.GlossEntry.Abbrev"],
)
def test_that_json_parser_can_delete_keys(template_and_parser, key):
    template, parser = template_and_parser("json", "glossary")

    parser.delete(key)

    assert parser.has(key) is False
