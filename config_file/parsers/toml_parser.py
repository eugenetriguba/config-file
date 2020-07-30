try:
    import tomlkit

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

from config_file.exceptions import MissingDependencyError

from .base_parser import BaseParser

class TomlParser(BaseParser):
    def __init__(self, file_contents: str):
        if not TOML_AVAILABLE:
            raise MissingDependencyError(
                "It doesn't appear `toml` is installed, but a toml "
                "file was attempted to be used. Install the `toml` "
                "extra first with `pip install config-file[toml]`."
            )

        super().__init__(
            file_contents=file_contents,
            module=tomlkit,
            # tomlkit doesn't expose it's exceptions, but
            # it's parsing error is a subclass of ValueError
            decode_error=ValueError,
        )
