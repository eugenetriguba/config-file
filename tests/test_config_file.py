import json
from pathlib import Path

import pytest

from config_file import ConfigFile, BaseParser


@pytest.mark.parametrize(
    "file_contents, file_name", [("[calendar]\nsunday_index = 0\n\n", "config.ini")]
)
def test_that_config_file_initializes_correctly(tmp_path, file_contents, file_name):
    temp = tmp_path / file_name
    temp.write_text(file_contents)

    config = ConfigFile(temp)
    assert config.path == str(temp)
    assert config.contents == temp.read_text()
    assert isinstance(config.parser, BaseParser)


@pytest.mark.parametrize(
    "file_contents, file_name, original_file_name",
    [("[calendar]\nsunday_index = 0\n\n", "config.ini", "config.original.ini")],
)
def test_that_config_file_can_restore_the_original(
    tmpdir, file_contents, file_name, original_file_name
):
    config_path = tmpdir / file_name
    config_path.write_text(file_contents, encoding="utf-8")

    original_config_path = tmpdir / original_file_name
    original_config_path.write_text(file_contents, encoding="utf-8")

    config = ConfigFile(str(config_path))
    config.set("calendar.sunday_index", 0)
    config.restore_original()
    assert config.stringify() == ConfigFile(str(original_config_path)).stringify()
    assert config_path.read_text(encoding="utf-8") == original_config_path.read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize(
    "file_extension, specify_original_config_path", [("ini", False), ("ini", True)]
)
def test_missing_config_files_during_restore(
    tmpdir, file_extension, specify_original_config_path
):
    with pytest.raises(OSError):
        temp_path = tmpdir / "config.{}".format(file_extension)
        temp_path.write("")
        config = ConfigFile(str(temp_path))

        if specify_original_config_path:
            specify_original_config_path = "does_not_exist.{}".format(file_extension)
        else:
            config.path = "does_not_exist.{}".format(file_extension)
            specify_original_config_path = None

        config.restore_original(original_file_path=specify_original_config_path)


@pytest.mark.parametrize(
    "file_contents, file_name", [("[calendar]\nsunday_index = 0\n\n", "config.ini")]
)
def test_that_config_file_can_save(tmpdir, file_contents, file_name):
    config_path = tmpdir / file_name
    config_path.write_text(file_contents, encoding="utf-8")

    config = ConfigFile(str(config_path))
    config.set("calendar.sunday_index", 1)
    config.save()
    assert config.stringify() == Path(config_path).read_text(encoding="utf-8")


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
    config = ConfigFile(str(config_path))

    ret_val = config.get(section_key, parse_types=parse_type, default=default)
    if return_type is not None:
        assert return_type(ret_val) == value
    else:
        assert ret_val == value


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
    tmpdir, file_extension, file_contents, section_key, expected_result
):
    config_path = tmpdir / "config.{}".format(file_extension)
    config_path.write_text(file_contents, encoding="utf-8")
    config = ConfigFile(str(config_path))
    assert config.has(section_key) == expected_result


@pytest.mark.parametrize(
    "section_key, file_name, file_contents, deleted_file_contents",
    [
        (
            "calendar.sunday_index",
            "config.ini",
            "[calendar]\nsunday_index = 0\n\n",
            "[calendar]\n\n",
        ),
        (
            "calendar.sunday_index",
            "config.json",
            json.dumps({"calendar": {"sunday_index": 0}}),
            json.dumps({"calendar": {}}),
        ),
    ],
)
def test_that_config_file_can_delete(
    tmpdir, section_key, file_name, file_contents, deleted_file_contents
):
    config_path = tmpdir / file_name
    config_path.write_text(file_contents, encoding="utf-8")
    config = ConfigFile(str(config_path))
    config.delete(section_key)
    assert config.stringify() == deleted_file_contents


@pytest.mark.parametrize(
    "path, is_dir", [("invalid", False), ("invalid", True), ("invalid.conf", False)]
)
def test_invalid_config_paths(tmpdir, path, is_dir):
    with pytest.raises(ValueError):
        temp_path = tmpdir / path
        temp_path.write("")
        ConfigFile(str(tmpdir)) if is_dir else ConfigFile(str(temp_path))


def test_that_custom_parser_can_be_used(tmpdir):
    class CustomParser(BaseParser):
        def __init__(self, file_contents):
            super().__init__(file_contents)

        def get(self, key, parse_types=True):
            return key

        def set(self, key, value):
            return key, value

        def delete(self, section_key):
            return section_key

        def has(self, section_key: str) -> bool:
            return True

        def stringify(self) -> str:
            return str(self.parsed_content)

        def parse(self, file_contents: str):
            return file_contents

    config_path = tmpdir / "config.conf"
    config_path.write_text("", encoding="utf-8")
    config = ConfigFile(str(config_path), parser=CustomParser)
    assert isinstance(config.parser, CustomParser)
    assert config.get("key") == "key"
    assert config.set("key", "value") == ("key", "value")
    assert config.delete("section_key") == "section_key"
    assert config.has("blah")
    assert config.stringify() == ""


def test_that_a_tidle_in_the_config_path_expands_to_the_absolute_path():
    config_name = "fjlajbkfdajfdioanfks.ini"
    config_path = "~/" + config_name

    try:
        Path(config_path).expanduser().touch()
        assert ConfigFile(config_path).path == str(Path.home() / config_name)
    finally:
        Path(config_path).expanduser().unlink()
