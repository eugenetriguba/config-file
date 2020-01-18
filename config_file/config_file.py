import inspect
from pathlib import Path

from config_file.parsers.base_parser import BaseParser
from config_file.parsers.ini_parser import IniParser
from config_file.utils import split_on_dot


class ConfigFile:
    def __init__(self, file_path: str, parser=None):
        self.path = self.__create_config_path(file_path)

        with open(self.path, "r") as file:
            self.contents = file.read()

        self.parser = self.__determine_parser(file_path, parser)

    @staticmethod
    def __create_config_path(file_path: str):
        if len(file_path) > 1 and file_path[0] == "~":
            return Path(file_path).expanduser().resolve()

        return Path(file_path)

    def __determine_parser(self, file_path: str, parser):
        if isinstance(parser, BaseParser) and not inspect.isabstract(parser):
            return parser(self.contents)

        file_type = split_on_dot(file_path)[-1]
        if file_type == "ini":
            return IniParser(self.contents)
        else:
            raise ValueError(
                f"File path contains an unsupported or "
                f"unrecognized file type: {file_path}"
            )

    def get(self, key, parse_type=True):
        """
        Retrieve the value of a key in its native type.
        This means the string 'true' will be parsed back as the
        boolean True.

        If parse_type is set to False, all values will be returned
        back as strings.
        """
        return self.parser.get(key, parse_type=parse_type)

    def set(self, key, value):
        """Sets the value of a key."""
        return self.parser.set(key, value)

    def delete(self, section_key):
        """Deletes a key/value pair or entire sections."""
        return self.parser.delete(section_key)

    def stringify(self) -> str:
        """Convert the parsed internal representation of the file back into a string."""
        return self.parser.stringify()

    def has(self, section_key: str) -> bool:
        """
        Check if a section, sub-section, or key exists in the file
        using a section.key format.

        Some formats, like JSON, do not have sections and therefore,
        it would only be checking if the section
        """
        return self.parser.has(section_key)
