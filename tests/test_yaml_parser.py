from unittest.mock import patch

import pytest

from config_file.yaml_parser import YamlParser


def test_that_import_error_is_raised_if_no_ruamelyaml():
    """
    config_file.yaml_parser.YamlParser

    Ensure an import error is raised if ruamel.yaml is not
    installed.
    """
    with pytest.raises(ImportError) as error:

        with patch("builtins.__import__") as mock_import:
            mock_import.side_effect = ImportError
            YamlParser("")

    assert (
        "Install the `yaml` extra first with `pip install config-file[yaml]`."
        in str(error)
    )
