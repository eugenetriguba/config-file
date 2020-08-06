try:
    from ruamel.yaml import YAML, YAMLError, round_trip_dump, round_trip_load

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from .base_parser import BaseParser
from .exceptions import MissingDependencyError


class YamlParser(BaseParser):
    def __init__(self, file_contents: str):
        if not YAML_AVAILABLE:
            raise MissingDependencyError(
                "It doesn't appear `ruamel.yaml` is installed, but a yaml "
                "file was attempted to be used. Install the `yaml` "
                "extra first with `pip install config-file[yaml]`."
            )

        yaml = YAML(typ="safe")
        yaml.loads = round_trip_load
        yaml.dumps = round_trip_dump

        super().__init__(
            file_contents=file_contents, module=yaml, decode_error=YAMLError
        )
