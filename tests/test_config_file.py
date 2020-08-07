import json
from pathlib import Path
from typing import Callable, Tuple

import pytest

from config_file.abstract_parser import AbstractParser
from config_file.config_file import ConfigFile
from config_file.ini_parser import IniParser

SUPPORTED_FILE_TYPES = ["ini", "json", "yaml", "toml"]


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def template_and_config_file(
    request, template_file
) -> Callable[[str], Tuple[Path, ConfigFile]]:
    """
    Fixture that is a wrapper around the template_file
    fixture. Using the function returned, we can retrieve
    a temporary file that has the contents of the specified
    template file as well as a ConfigFile with the template
    already passed in.

    This fixture will make the test function run once for every
    supported file type, each with the corresponding template
    in the different file type.
    """

    def func(template_name: str = "default"):
        template = template_file(request.param, template_name)
        return template, ConfigFile(template)

    return func


@pytest.fixture(params=SUPPORTED_FILE_TYPES)
def templated_config_file(template_and_config_file) -> Callable[[str], ConfigFile]:
    """
    Wrapper around template_and_config_file for when we
    only need the ConfigFile and not the template.
    """

    def func(template_name: str = "default"):
        return template_and_config_file(template_name)[1]

    return func


def test_that_config_file_is_initialized_correctly(template_and_config_file):
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that an initialized ConfigFile has the
    correct file path and has a parser that is a AbstractParser.
    """
    template_file, config = template_and_config_file()

    assert config.file_path == template_file
    assert isinstance(config._ConfigFile__parser, AbstractParser)


def test_that_a_tidle_in_the_config_path_expands_to_the_absolute_path():
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that a home tilde (~) in a file path passed
    to ConfigFile is expanded to the full path.
    """
    config_name = "temp.ini"
    config_path = "~/" + config_name

    try:
        Path(config_path).expanduser().touch()
        assert ConfigFile(config_path).file_path == Path.home() / config_name
    finally:
        Path(config_path).expanduser().unlink()


@pytest.mark.parametrize("path", ["invalid", "invalid.conf"])
def test_invalid_path_raises_file_not_found_error(path):
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that when a path to a file that does not exist
    that is passed into the constructor, it raises a FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        ConfigFile(path)


def test_directory_raises_value_error():
    """
    config_file.config_file.ConfigFile.__init__

    Ensure when a path to a directory is passed into
    the constructor, it raises a ValueError.
    """
    with pytest.raises(ValueError):
        ConfigFile(".")


def test_that_config_file_can_save(template_and_config_file):
    """
    config_file.config_file.ConfigFile.save

    Ensure that altering the configuration file and saving it
    writes those changes out to the filesystem.
    """
    template_file, config = template_and_config_file()

    config.set("header_one.number_key", 25)
    config.save()

    assert config.stringify() == template_file.read_text()


def test_that_config_file_can_restore_the_original(
    templated_config_file, template_original_file
):
    """
    config_file.config_file.ConfigFile.restore_original

    Ensure that we can restore the "original" configuration
    file, using the calculated path and after altering the
    internal config contents. Those internal contents and file
    should be reset to the original file.
    """
    config = templated_config_file()
    original_file = template_original_file(config.file_path)

    config.set("header_one.number_key", 5)
    config.restore_original()

    assert config.stringify() == original_file.read_text()
    assert config.file_path.read_text() == original_file.read_text()


def test_missing_config_file_during_restore(templated_config_file):
    """
    config_file.config_file.ConfigFile.restore_original

    Ensure that if we try to restore_original without using
    the optional original_file_path argument but we do not
    have a file at the calculated default path, a FileNotFoundError
    is raised.
    """
    config = templated_config_file()

    with pytest.raises(FileNotFoundError) as error:
        config.restore_original()

    assert "The specified config file" in str(error)
    assert "does not exist" in str(error)


@pytest.mark.parametrize("key", ["header_one", "header_one.number_key"])
def test_that_config_file_has_can_find_sections_and_keys_that_exist(
    templated_config_file, key
):
    """
    config_file.config_file.ConfigFile.has

    Ensure that when a section or key that exists
    is passed to has(), it can find it and returns True.
    """
    config = templated_config_file()
    assert config.has(key)


def test_that_config_file_has_returns_false_for_sections_and_keys_that_do_not_exist(
    templated_config_file,
):
    """
    config_file.config_file.ConfigFile.has

    Ensure that when a section or key that does not exist
    is passed to has(), it can't find it and returns False.
    """
    config = templated_config_file()
    assert not config.has("header_one.blah")


@pytest.mark.parametrize(
    "key, value",
    [
        ("header_one.number_key", 0),
        ("header_two.list_key", [1, 2, 3]),
        ("header_one", {"number_key": 0}),
    ],
)
def test_that_config_file_can_get_existent_keys(templated_config_file, key, value):
    """
    config_file.config_file.ConfigFile.get

    Ensure that we can retrieve a section or key
    and that it is in its native type (the type that
    it was set to).

    The one caveat here is the IniParser. The IniParser
    uses configparser under the hood which simply always
    returns back a string. However, that is not the case
    for JsonParser, YamlParser, or TomlParser.
    """
    config = templated_config_file()

    if isinstance(config._ConfigFile__parser, IniParser):
        if type(value) is not dict:
            # not a section being retrieved
            value = str(value)
        else:
            # section is being retrieved so it should be a dict
            # but the values inside should be strings.
            value = json.loads(json.dumps(value), parse_int=str)

    assert config.get(key) == value


@pytest.mark.parametrize("key", ["header_one.number_key", "header_one"])
def test_that_config_file_can_delete(templated_config_file, key):
    """
    config_file.config_file.ConfigFile.delete

    Ensure that we can delete keys and that they are removed
    from the internal contents of the ConfigFile.
    """
    config = templated_config_file()

    config.delete(key)

    assert config.has(key) is False


@pytest.mark.parametrize("key", ["", 0, False, {}, "header_one.does_not_exist"])
def test_that_config_file_raises_key_error_on_invalid_input_or_missing_key(
    templated_config_file, key
):
    """
    config_file.config_file.ConfigFile.delete

    Ensure that a KeyError is raised if we
    tried to provide a value that is not valid
    (like the wrong type so it is an invalid key)
    or one that does not exist.
    """
    config = templated_config_file()

    with pytest.raises(KeyError):
        config.delete(key)
