from .base_parser import BaseParser


class YamlParser(BaseParser):
    def __init__(self, file_contents: str):
        try:
            from ruamel.yaml import YAML, YAMLError, round_trip_dump, round_trip_load

            yaml = YAML(typ="safe")
            yaml.loads = round_trip_load
            yaml.dumps = round_trip_dump

            super().__init__(
                file_contents=file_contents, module=yaml, decode_error=YAMLError
            )
        except ImportError:
            raise ImportError(
                "It doesn't appear `ruamel.yaml` is installed, but a yaml "
                "file was attempted to be used. Install the `yaml` "
                "extra first with `pip install config-file[yaml]`."
            )
