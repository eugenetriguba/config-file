import json
from pathlib import Path
from typing import Callable, Tuple

import pytest

from config_file.abstract_parser import AbstractParser
from config_file.config_file import ConfigFile
from config_file.exceptions import ParsingError
from config_file.ini_parser import IniParser
from config_file.config_file_path import ConfigFilePath

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


def test_config_file_init_has_correct_path_and_parser(template_and_config_file):
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that an initialized ConfigFile has the
    correct file path and has a parser that is a AbstractParser.
    """
    template_file, config = template_and_config_file()

    assert config.path == template_file
    assert isinstance(config._ConfigFile__parser, AbstractParser)


@pytest.mark.parametrize("file_type", SUPPORTED_FILE_TYPES)
def test_config_file_raises_error_on_malformed_file(template_file, file_type):
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that a ParsingError is raised on a malformed file.
    """
    with pytest.raises(ParsingError):
        ConfigFile(template_file(file_type, template_name="invalid"))


def test_config_file_expands_home_tildes_in_path():
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that a home tilde (~) in a file path passed
    to ConfigFile is expanded to the full path.
    """
    config_name = "temp.ini"
    config_path = "~/" + config_name

    try:
        Path(config_path).expanduser().touch()
        assert ConfigFile(config_path).path == Path.home() / config_name
    finally:
        Path(config_path).expanduser().unlink()


@pytest.mark.parametrize("path", ["invalid", "invalid.conf"])
def test_config_file_raises_error_on_non_existent_path(path):
    """
    config_file.config_file.ConfigFile.__init__

    Ensure that when a path to a file that does not exist
    that is passed into the constructor, it raises a FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        ConfigFile(path)


def test_config_file_raises_error_if_path_is_directory():
    """
    config_file.config_file.ConfigFile.__init__

    Ensure when a path to a directory is passed into
    the constructor, it raises a ValueError.
    """
    with pytest.raises(ValueError):
        ConfigFile(".")


@pytest.mark.parametrize(
    "key, value",
    [
        ("header_one.list_key", "different value"),
        ("header_one", {}),
        ("header_one.number_key", 1),
    ],
)
def test_set_can_add_to_or_alter_the_file(templated_config_file, key, value):
    """
    config_file.config_file.ConfigFile.set

    Ensure that for the keys we can, we retrieve that same value back 
    (with the exception of ini, which should always be a string).
    """
    config = templated_config_file()
    config.set(key, value)

    # configparser treats everything as a string. Make
    # sure we're entering in files in the dict as a str.
    if ConfigFilePath(config.path).extension == "ini":
        if isinstance(value, (int, float)):
            value = str(value)

        assert config.get(key) == value
    else:
        assert config.get(key) == value


def test_config_file_can_save(template_and_config_file):
    """
    config_file.config_file.ConfigFile.save

    Ensure that altering the configuration file and saving it
    writes those changes out to the filesystem.
    """
    template_file, config = template_and_config_file()

    config.set("header_one.number_key", 25)
    config.save()

    assert config.stringify() == template_file.read_text()


def test_restore_original_can_restore_with_calculated_in_path(
    templated_config_file, template_original_file
):
    """
    config_file.config_file.ConfigFile.restore_original

    Ensure that we can restore the "original" configuration
    file, using the *calculated* path, after altering the
    internal config contents.

    Those internal contents and file should be reset to the
    original file.
    """
    config = templated_config_file()
    original_file = template_original_file(config.path)

    config.set("header_one.number_key", 5)
    config.restore_original()

    assert config.stringify() == original_file.read_text()
    assert config.path.read_text() == original_file.read_text()


@pytest.mark.parametrize("file_type", SUPPORTED_FILE_TYPES)
def test_restore_original_can_restore_with_passed_in_path(
    template_file, tmp_file, file_type
):
    """
    config_file.config_file.ConfigFile.restore_original

    Ensure that we can restore the "original" configuration
    file, using the *passed* in path, after altering the
    internal config contents.
    """
    config_file = template_file(file_type)
    config = ConfigFile(config_file)

    original_file = tmp_file(f"file.{file_type}", config_file.read_text())
    original_config = ConfigFile(original_file)
    original_config.set("some_new_section.some_new_key", 5)
    original_config.save()

    config.restore_original(original_path=original_file)

    assert config.stringify() == original_config.stringify()
    assert config.path.read_text() == original_file.read_text()


def test_restore_original_raises_error_on_missing_file(templated_config_file):
    """
    config_file.config_file.ConfigFile.restore_original

    Ensure that if we try to restore_original without using
    the optional original_path argument but we do not
    have a file at the calculated default path, a FileNotFoundError
    is raised.
    """
    config = templated_config_file()

    with pytest.raises(FileNotFoundError) as error:
        config.restore_original()

    assert "The specified config file" in str(error)
    assert "does not exist" in str(error)


@pytest.mark.parametrize("key", ["header_one", "header_one.number_key"])
def test_has_can_find_sections_and_keys(templated_config_file, key):
    """
    config_file.config_file.ConfigFile.has

    Ensure that when a section or key that exists
    is passed to has(), it can find it and returns True.
    """
    config = templated_config_file()
    assert config.has(key)
    assert key in config


def test_has_returns_false_for_sections_and_keys_that_do_not_exist(
    templated_config_file,
):
    """
    config_file.config_file.ConfigFile.has

    Ensure that when a section or key that does not exist
    is passed to has(), it can't find it and returns False.
    """
    config = templated_config_file()
    assert not config.has("header_one.blah")


def test_has_can_search_for_a_key_anywhere(templated_config_file):
    """
    config_file.config_file.ConfigFile.has

    Ensure that the wild=True keyword argument to has()
    retrieves if we have the key anywhere in the file.
    """
    config = templated_config_file()
    assert config.has("list_key", wild=True)


@pytest.mark.parametrize(
    "key, value",
    [
        ("header_one.number_key", 0),
        ("header_two.list_key", [1, 2, 3]),
        ("header_one", {"number_key": 0}),
    ],
)
def test_get_can_retrieve_existent_keys(templated_config_file, key, value):
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


def test_get_can_parse_all_types(templated_config_file):
    """
    config_file.config_file.ConfigFile.get

    Ensure we're able to parse out all the different types that
    may be used in a configuration file with the parse_types option.
    """
    config = templated_config_file(template_name="all_strings")
    output = {"list": [], "dict": {}, "num": 5, "bool": False, "float": 5.5}

    assert config.get("header", parse_types=True) == output


def test_get_can_use_a_default(templated_config_file):
    config = templated_config_file()
    assert config.get("does_not_exist", default="default!") == "default!"


def test_get_raises_a_key_error_on_invalid_key(templated_config_file):
    config = templated_config_file()

    with pytest.raises(KeyError):
        config.get("does_not_exist")


@pytest.mark.parametrize("key", ["header_one.number_key", "header_one"])
def test_delete_can_remove_sections_and_keys(templated_config_file, key):
    """
    config_file.config_file.ConfigFile.delete

    Ensure that we can delete keys and that they are removed
    from the internal contents of the ConfigFile.
    """
    config = templated_config_file()

    config.delete(key)

    assert config.has(key) is False


@pytest.mark.parametrize("key", ["", 0, False, {}, "header_one.does_not_exist"])
def test_delete_raises_key_error_on_invalid_input_or_missing_key(
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


def test_keys_can_be_set_with_array_notation(template_and_config_file):
    """
    config_file.config_file.ConfigFile.__setitem__

    Ensure that the ConfigFile exposes its parsed contents
    using an array notation so we can set keys that way.
    """
    template_file, config = template_and_config_file()

    config["header_one"] = {}
    config.save()

    assert config.stringify() == template_file.read_text()


def test_keys_can_be_retrieved_with_array_notation(templated_config_file):
    """
    config_file.config_file.ConfigFile.__getitem__

    Ensure that the ConfigFile exposes its parsed contents
    using an array notation so we can retrieve keys that way.
    """
    config = templated_config_file()
    assert int(config["header_one"]["number_key"]) == 0


def test_keys_can_be_deleted_with_array_notation(templated_config_file):
    """
    config_file.config_file.ConfigFile.__delitem__

    Ensure that the ConfigFile exposes its parsed contents
    using an array notation so we can delete keys that way.
    """
    config = templated_config_file()
    del config["header_one"]

    with pytest.raises(KeyError):
        config["header_one"]


def test_the_config_file_can_be_stringified(template_and_config_file):
    """
    config_file.config_file.ConfigFile.__str__
    config_file.config_file.ConfigFile.__repr__
    config_file.config_file.ConfigFile.stringify()

    Ensure that the stringified version of the config file
    is the string version of the file and that the repr also
    includes the file path.
    """
    template, config = template_and_config_file()
    assert template.read_text() == str(config)
    assert template.read_text() == config.stringify()
    assert f"{str(template)}\n\n{str(config)}" == repr(config)
