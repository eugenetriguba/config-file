from typing import Type

from .base_parser import BaseParser


class YamlParser(BaseParser):
    def __init__(self, file_contents: str):
        try:
            super().__init__(file_contents)
        except ImportError:
            raise ImportError(
                "It doesn't appear `ruamel.yaml` is installed, but a yaml "
                "file was attempted to be used. Install the `yaml` "
                "extra first with `pip install config-file[yaml]`."
            )

    @property
    def decode_error(self) -> Type[Exception]:
        from ruamel.yaml import YAMLError

        return YAMLError

    def loads(self, contents: str) -> dict:
        from ruamel.yaml import round_trip_load

        return round_trip_load(contents)

    def dumps(self, loaded_contents: dict) -> str:
        from ruamel.yaml import round_trip_dump

        return round_trip_dump(loaded_contents)
