from .base_parser import BaseParser


class TomlParser(BaseParser):
    def __init__(self, file_contents: str):
        try:
            import tomlkit
            from tomlkit.exceptions import ParseError

            super().__init__(
                file_contents=file_contents, module=tomlkit, decode_error=ParseError,
            )
        except ImportError:
            raise ImportError(
                "It doesn't appear `tomlkit` is installed, but a toml "
                "file was attempted to be used. Install the `toml` "
                "extra first with `pip install config-file[toml]`."
            )
