from unittest.mock import patch

import pytest

from config_file.toml_parser import TomlParser


def test_that_import_error_is_raised_if_no_tomlkit():
    """
    config_file.toml_parser.TomlParser

    Ensure an import error is raised if tomlkit is not
    installed.
    """
    with pytest.raises(ImportError) as error:

        with patch("builtins.__import__") as mock_import:
            mock_import.side_effect = ImportError
            TomlParser("")

    assert (
        "Install the `toml` extra first with `pip install config-file[toml]`."
        in str(error)
    )
