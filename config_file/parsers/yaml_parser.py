try:
    import yaml

    YAML_AVAILABLE = True

    # Conform yaml to json and
    # toml package syntax
    yaml.loads = yaml.load
    yaml.dumps = yaml.dump
except ImportError:
    YAML_AVAILABLE = False

from config_file.exceptions import MissingDependencyError

from .base_parser import BaseParser


class YamlParser(BaseParser):
    def __init__(self, file_contents: str):
        if not YAML_AVAILABLE:
            raise MissingDependencyError(
                "It doesn't appear `PyYaml` is installed, but a yaml "
                "file was attempted to be used. Install the `toml` "
                "extra first with `pip install config-file[toml]`."
            )

        super().__init__(
            file_contents=file_contents, module=yaml, decode_error=yaml.YAMLError
        )
