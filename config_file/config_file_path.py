import os
from pathlib import Path as _Path_
from pathlib import _posix_flavour, _windows_flavour
from typing import Type

from config_file.abstract_parser import AbstractParser
from config_file.ini_parser import IniParser
from config_file.json_parser import JsonParser
from config_file.toml_parser import TomlParser
from config_file.yaml_parser import YamlParser

from .utils import split_on_dot


class ConfigFilePath(_Path_):
    """A ConfigFilePath object, which subclasses Path.

    It provides us easy ways to grab the original config file
    path, file extension, validate the path, or determine the parser
    that should be use for the given file type.

    See https://codereview.stackexchange.com/questions/162426/subclassing-pathlib-path
    for more details on subclassing the pathlib.Path object.
    """

    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    @property
    def original_path(self) -> "ConfigFilePath":
        """Computes the original configuration file path.

        e.g. ConfigFilePath("./config.ini").original_path -> "./config.original.ini"

        Returns:
            The path to the original configuration file, which
            may or may not exist.
        """
        file_parts = split_on_dot(self, only_last_dot=True)
        file_parts.insert(-1, "original")
        return ConfigFilePath(".".join(file_parts))

    @property
    def extension(self) -> str:
        """Retrieves the extension of the file
        path we passed in, without the '.'.

        e.g. ConfigFilePath("./pyproject.toml").extension -> "toml"

        Returns:
            The extension of the current file path.
        """
        _, extension = os.path.splitext(str(self))
        return extension[1:]

    @property
    def parser(self) -> Type[AbstractParser]:
        """Determine what parser should be used for this file.

        Raises:
            ValueError: If the extension of the file is not recognized.
            ParsingError: If the contents could not be parsed.

        Returns:
            The instantiated parser that should be used for this file.
        """
        if self.extension == "":
            raise ValueError(
                "Tried to determine a parser to use, but the file at "
                f"{self} does not have an extension."
            )

        if self.extension == "ini":
            return IniParser(self.contents)
        elif self.extension == "json":
            return JsonParser(self.contents)
        elif self.extension == "yaml" or self.extension == "yml":
            return YamlParser(self.contents)
        elif self.extension == "toml":
            return TomlParser(self.contents)
        else:
            raise ValueError(
                f"File path at `{self}` contains an unrecognized file type."
            )

    @property
    def contents(self) -> str:
        """Retrieve the contents of the file.

        Returns:
            The contents of the file at this path.
        """
        with open(self, "r") as file:
            return file.read()

    def validate(self) -> "ConfigFilePath":
        """Validates that the current path exists, is a directory,
        and expands any home tidles.

        Raises:
            FileNotFoundError: If the path does not exist.
            ValueError: If the path leads to a directory.

        Returns:
            A ConfigFilePath object with any ~'s expanded.
        """
        if len(self.parts) >= 1 and self.parts[0] == "~":
            self = ConfigFilePath(self.expanduser())

        if not self.exists():
            raise FileNotFoundError(
                f"The specified config file ({self}) does not exist."
            )

        if self.is_dir():
            raise ValueError(f"The specified config file ({self}) is a directory")

        return self
