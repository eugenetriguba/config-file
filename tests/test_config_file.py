import json
from pathlib import Path

import pytest

from config_file.config_file import ConfigFile
from config_file.parsers.abstract_parser import AbstractParser

SUPPORTED_FILE_TYPES = ["ini", "json", "yaml", "toml"]


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def template_and_config_file(request, template_file):
    def func(template_name: str = "default", parser: AbstractParser = None):
        template = template_file(request.param, template_name)
        return template, ConfigFile(template, parser=parser)

    return func


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def templated_config_file(template_and_config_file):
    def func(template_name: str = "default", parser: AbstractParser = None):
        return template_and_config_file(template_name, parser)[1]

    return func


def test_that_config_file_is_initialized_correctly(template_and_config_file):
    template_file, config = template_and_config_file()

    assert config.path == template_file
    assert config.stringify() == template_file.read_text()
    assert isinstance(config._ConfigFile__parser, AbstractParser)


def test_that_a_tidle_in_the_config_path_expands_to_the_absolute_path():
    config_name = "temp.ini"
    config_path = "~/" + config_name

    try:
        Path(config_path).expanduser().touch()
        assert ConfigFile(config_path).path == Path.home() / config_name
    finally:
        Path(config_path).expanduser().unlink()


@pytest.mark.skip(msg="needs fixing up")
@pytest.mark.parametrize("path", ["", "invalid", "invalid.conf"])
def test_invalid_config_paths(path):
    with pytest.raises(ValueError):
        ConfigFile(path)


def test_that_config_file_can_save(template_and_config_file):
    template_file, config = template_and_config_file()

    config.set("header_one.number_key", 25)
    config.save()

    assert config.stringify() == template_file.read_text()


def test_that_config_file_can_restore_the_original(
    templated_config_file, template_original_file
):
    config = templated_config_file()
    original_file = template_original_file(config.path)

    config.set("header_one.number_key", 5)
    config.restore_original()

    assert config.stringify() == original_file.read_text()


def test_missing_config_file_during_restore(templated_config_file):
    config = templated_config_file()

    with pytest.raises(FileNotFoundError) as error:
        config.restore_original()

    assert "file to restore to does not exist" in str(error)


@pytest.mark.parametrize(
    "file_extension, file_contents, section_key, expected_result",
    [
        ("ini", "[calendar]\nsunday_index = 0\n\n", "calendar.sunday_index", True),
        ("ini", "[calendar]\nsunday_index = 0\n\n", "calendar.blah", False),
        ("ini", "[calendar]\nsunday_index = 0\n\n", "calendar", True),
        ("json", json.dumps({"calendar": {"sunday_index": 0}}), "calendar", True),
        ("json", json.dumps({"calendar": {"sunday_index": 0}}), "blah", False),
        ("json", json.dumps({"calendar": {"sunday_index": 0}}), "sunday_index", True),
    ],
)
def test_that_config_file_can_find_sections_and_keys(
    tmp_file, file_extension, file_contents, section_key, expected_result
):
    config = ConfigFile(tmp_file(f"file.{file_extension}", file_contents))
    assert config.has(section_key) == expected_result


@pytest.mark.parametrize(
    "section_key, value, parse_type, return_type, default, file_name, file_contents",
    [
        (
            "calendar.sunday_index",
            0,
            True,
            None,
            False,
            "config.ini",
            "[calendar]\nsunday_index = 0\n\n",
        ),
        (
            "calendar.sunday_index",
            "0",
            False,
            None,
            False,
            "config.ini",
            "[calendar]\nsunday_index = 0\n\n",
        ),
        (
            "calendar.sunday_index",
            0,
            False,
            None,
            False,
            "config.json",
            json.dumps({"calendar": {"sunday_index": 0}}),
        ),
        (
            "calendar.missing",
            "my default value",
            False,
            None,
            "my default value",
            "config.json",
            json.dumps({"calendar": 5}),
        ),
        (
            "calendar.sunday_index",
            0,
            False,
            int,
            False,
            "config.ini",
            "[calendar]\nsunday_index = 0\n\n",
        ),
    ],
)
def test_that_config_file_can_get(
    tmpdir,
    section_key,
    value,
    return_type,
    parse_type,
    file_name,
    file_contents,
    default,
):
    config_path = tmpdir / file_name
    config_path.write_text(file_contents, encoding="utf-8")
    config = ConfigFile(config_path)

    ret_val = config.get(section_key, parse_types=parse_type, default=default)
    if return_type is not None:
        assert return_type(ret_val) == value
    else:
        assert ret_val == value


def test_that_config_file_can_delete(templated_config_file):
    config = templated_config_file()

    config.delete("header_one.number_key")

    assert config.has("header_one.number_key") is False


# def test_that_custom_parser_can_be_used(template_and_config_file):
#     class CustomParser(AbstractParser):
#         def __init__(self, file_contents):
#             super().__init__(file_contents)
#
#         def parse(self, file_contents: str):
#             return file_contents
#
#         def get(self, key, parse_types=True):
#             return key
#
#         def set(self, key, value):
#             return key, value
#
#         def delete(self, section_key):
#             return section_key
#
#         def has(self, section_key: str) -> bool:
#             return True
#
#         def stringify(self) -> str:
#             return str(self.parsed_content)
#
#     template_file, config = template_and_config_file(parser=CustomParser)
#
#     assert isinstance(config._ConfigFile__parser, CustomParser)
#     assert config.get("key") == "key"
#     assert config.set("key", "value") == ("key", "value")
#     assert config.delete("section_key") == "section_key"
#     assert config.has("blah")
#     assert config.stringify() == template_file.read_text()
