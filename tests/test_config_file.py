from pathlib import Path

import pytest

from config_file.abstract_parser import AbstractParser
from config_file.config_file import ConfigFile
from config_file.exceptions import MissingKeyError

SUPPORTED_FILE_TYPES = ["ini", "json", "yaml", "toml"]


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def template_and_config_file(request, template_file):
    def func(template_name: str = "default"):
        template = template_file(request.param, template_name)
        return template, ConfigFile(template)

    return func


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def templated_config_file(template_and_config_file):
    def func(template_name: str = "default"):
        return template_and_config_file(template_name)[1]

    return func


def test_that_config_file_is_initialized_correctly(template_and_config_file):
    template_file, config = template_and_config_file()

    assert config.file_path == template_file
    assert config.stringify() == template_file.read_text()
    assert isinstance(config._ConfigFile__parser, AbstractParser)


def test_that_a_tidle_in_the_config_path_expands_to_the_absolute_path():
    config_name = "temp.ini"
    config_path = "~/" + config_name

    try:
        Path(config_path).expanduser().touch()
        assert ConfigFile(config_path).file_path == Path.home() / config_name
    finally:
        Path(config_path).expanduser().unlink()


@pytest.mark.parametrize("path", ["invalid", "invalid.conf"])
def test_invalid_path_raises_file_not_found_error(path):
    with pytest.raises(FileNotFoundError):
        ConfigFile(path)


@pytest.mark.parametrize("path", [""])
def test_directory_raises_value_error(path):
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
    original_file = template_original_file(config.file_path)

    config.set("header_one.number_key", 5)
    config.restore_original()

    assert config.stringify() == original_file.read_text()


def test_missing_config_file_during_restore(templated_config_file):
    config = templated_config_file()

    with pytest.raises(FileNotFoundError) as error:
        config.restore_original()

    assert "The specified config file" in str(error)
    assert "does not exist" in str(error)


@pytest.mark.parametrize(
    "key, expected_result",
    [
        ("header_one", True),
        ("header_one.number_key", True),
        ("header_one.blah", False),
    ],
)
def test_that_config_file_can_find_sections_and_keys(
    templated_config_file, key, expected_result
):
    config = templated_config_file()
    assert config.has(key) == expected_result


# @pytest.mark.parametrize(
#     "key, value",
#     [
#         ("header_one.number_key", 0),
#         ("header_two.list_key", [1, 2, 3]),
#     ],
# )
# def test_that_config_file_can_get_existent_keys(templated_config_file, key, value):
#     config = templated_config_file()
#
#     print(config.get(key))
#     print(type(config.get(key)))
#     print(config._ConfigFile__parser)
#
#     assert config.get(key) == value


@pytest.mark.parametrize("key", ["header_one.number_key", "header_one"])
def test_that_config_file_can_delete(templated_config_file, key):
    config = templated_config_file()

    config.delete(key)

    assert config.has(key) is False


@pytest.mark.parametrize("key", ["", 0, False, {}, "header_one.does_not_exist"])
def test_that_config_file_raises_missing_key_error_on_invalid_input_or_missing_key(
    templated_config_file, key
):
    config = templated_config_file()

    with pytest.raises(MissingKeyError):
        config.delete(key)
