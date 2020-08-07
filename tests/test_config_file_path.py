import os
from pathlib import Path, _posix_flavour, _windows_flavour

import pytest

from config_file.config_file_path import ConfigFilePath
from config_file.ini_parser import IniParser
from config_file.json_parser import JsonParser
from config_file.toml_parser import TomlParser
from config_file.yaml_parser import YamlParser


def test_config_file_path_is_a_path():
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that the ConfigFilePath object is an instance
    of Path from pathlib.
    """
    assert isinstance(ConfigFilePath("."), Path)


def test_config_file_path_has_the_correct_flavour():
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that the ConfigFilePath object has the
    correct Path flavor (since Path is actually
    swapped out, depending on the operating system,
    to a Posix flavour or Windows flavour)
    """
    path = ConfigFilePath(".")

    assert path._flavour == _windows_flavour if os.name == "nt" else _posix_flavour


def test_config_file_path_is_able_to_read_the_contents(template_file):
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that the contents retrieved are the same
    as the contents of the file.
    """
    template = template_file("ini", "default")
    path = ConfigFilePath(template)

    assert path.contents == template.read_text()


def test_config_file_path_is_able_to_calculate_the_original_path():
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that the calculated original configuration
    path includes a "original" between the filename and
    extension.
    """
    path = ConfigFilePath("path-existing-does-not-matter.txt")

    assert str(path.original_path) == "path-existing-does-not-matter.original.txt"


def test_config_file_path_is_able_to_retrieve_the_extension():
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that the retrieved extension is correct
    for the given filepath and that it does not retrieve
    the dot (.) from the extension.
    """
    path = ConfigFilePath("some-file.txt")

    assert path.extension == "txt"


@pytest.mark.parametrize(
    "template_file_type, expected_parser_type",
    [
        ("ini", IniParser),
        ("json", JsonParser),
        ("yaml", YamlParser),
        ("toml", TomlParser),
    ],
)
def test_config_file_path_decides_on_the_correct_parser(
    template_file, template_file_type, expected_parser_type
):
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that a filepath with an extension that is supported
    retrieves the correct parser for it.
    """
    template = template_file(template_file_type, "default")
    path = ConfigFilePath(template)

    assert isinstance(path.parser, expected_parser_type)


@pytest.mark.parametrize("filename", ["some-file", "some-file.unsupported-extension"])
def test_config_file_path_raises_value_error_on_parser_if_invalid_extension(filename):
    """
    config_file.config_file_path.ConfigFilePath

    Ensure that a ValueError is raised if we have a
    filepath with no extension or a filepath with an
    unsupported extension.
    """
    path = ConfigFilePath(filename)

    with pytest.raises(ValueError):
        path.parser
