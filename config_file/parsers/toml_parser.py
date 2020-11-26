from typing import Type

from .base_parser import BaseParser


class TomlParser(BaseParser):
    def __init__(self, file_contents: str):
        try:
            super().__init__(file_contents)
        except ImportError:
            raise ImportError(
                "It doesn't appear `tomlkit` is installed, but a toml "
                "file was attempted to be used. Install the `toml` "
                "extra first with `pip install config-file[toml]`."
            )

    @property
    def decode_error(self) -> Type[Exception]:
        from tomlkit.exceptions import ParseError

        return ParseError

    def loads(self, contents: str) -> dict:
        import tomlkit

        return tomlkit.loads(contents)

    def dumps(self, loaded_contents: dict) -> str:
        import tomlkit

        return tomlkit.dumps(loaded_contents)
