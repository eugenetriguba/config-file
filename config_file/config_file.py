import inspect
from pathlib import Path, PurePath
from shutil import copyfile

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.ini_parser import IniParser
from config_file.parsers.json_parser import JsonParser
from config_file.utils import split_on_dot


class ConfigFile:
    def __init__(self, file_path, parser: BaseParser = None):
        """
        Saves the config file path and expands it if needed, reads in
        the file contents, and determines what parser should be used for
        the given file.

        :param file_path: The path to your configuration file.
        :param parser: A custom parser you'd like used for your config file.
                      It must be a concrete implementation of BaseParser.

        :raises ValueError: If the specified file path does not have an extension
                            that is supported or it is a directory.
        """
        self.path = self.__create_config_path(file_path)
        self.contents = self.__read_config_file()
        self.parser = self.__determine_parser(file_path, parser)

    @staticmethod
    def __create_config_path(file_path, original: bool = False) -> str:
        if isinstance(file_path, PurePath):
            file_path = str(file_path)

        if len(file_path) > 1 and file_path[0] == "~":
            return str(Path(file_path).expanduser())

        if original:
            file_parts = split_on_dot(file_path, only_last_dot=True)
            file_parts.insert(-1, "original")
            file_path = ".".join(file_parts)

        if Path(file_path).is_dir():
            raise ValueError(f"The specified config file ({file_path}) is a directory.")

        return file_path

    def __determine_parser(self, file_path, parser: BaseParser):
        if isinstance(file_path, PurePath):
            file_path = str(file_path)

        if parser is not None and not inspect.isabstract(parser):
            return parser(self.contents)

        file_type = split_on_dot(file_path, only_last_dot=True)[-1]
        if file_type == "ini":
            return IniParser(self.contents)
        elif file_type == "json":
            return JsonParser(self.contents)
        else:
            raise ValueError(
                f"File path contains an unsupported or "
                f"unrecognized file type: {file_path}"
            )

    def __read_config_file(self):
        with open(self.path, "r") as file:
            return file.read()

    def get(self, key: str, parse_types: bool = False, return_type=None, default=None):
        """
        Retrieve the value of a key.

        :param key: The key to retrieve.
        :param parse_types: Automatically parse ints, floats, booleans, dicts, and
                           lists. This recursively parses all types in whatever you're
                           retrieving, not just a single type. e.g. If you are
                           retrieving a section, all values in that section with be
                           parsed.
        :param return_type: The type to coerce the return value to.
        :param default: The default value to return if the value of the key is empty.

        :return: The value of the key.
        """
        if default is None:
            key_value = self.parser.get(key, parse_types=parse_types)
        else:
            try:
                key_value = self.parser.get(key, parse_types=parse_types)
            except ParsingError:
                return default

        return return_type(key_value) if return_type else key_value

    def set(self, key: str, value):
        """Sets the value of a key."""
        return self.parser.set(key, value)

    def delete(self, section_key: str):
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
        it would only be checking if the key exists.
        """
        return self.parser.has(section_key)

    def restore_original(self, original_file_path=None):
        """
        Restores the original the config file by deleting it and copying the original
        back in its place. The internal contents of this config file object are then set
        to the newly reset config file.

        :param original_file_path: The path to the original config file to reset it to.
        If this is not provided and, say, your configuration file is config.json, the
        method would look for a config.original.json in the same folder by default.

        :return: True if the reset succeeded
        :raises OSError: If the original configuration file is not present or if an
                         error occurred when trying to copy the file.
        """
        if original_file_path is None:
            original_file_path = self.__create_config_path(
                str(self.path), original=True
            )

        if not Path(original_file_path).exists():
            raise OSError(
                f"The {original_file_path} file to restore to does not exist."
            )

        Path(self.path).expanduser().unlink()
        copyfile(original_file_path, self.path)
        self.contents = self.__read_config_file()
        self.parser.parsed_content = self.parser.parse(self.contents)

        return True

    def save(self):
        """
        Save the configuration changes by writing the file out to the specified path
        :return: True if the save succeeded.
        """
        with open(self.path, "w") as config_file:
            config_file.write(self.parser.stringify())

        return True
