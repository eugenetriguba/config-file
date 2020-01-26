from pathlib import Path

import pytest

from config_file.config_file import BaseParser, ConfigFile


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
    "path, is_dir", [("invalid", False), ("invalid", True), ("invalid.conf", False)]
)
def test_invalid_config_paths(tmpdir, path, is_dir):
    with pytest.raises(ValueError):
        temp_path = tmpdir / path
        temp_path.write("")
        ConfigFile(str(tmpdir)) if is_dir else ConfigFile(str(temp_path))
