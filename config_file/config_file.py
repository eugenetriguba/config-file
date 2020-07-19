import inspect
from pathlib import Path, PurePath
from shutil import copyfile
from typing import Any, Type, Union

from config_file.exceptions import ParsingError
from config_file.parsers import AbstractParser, IniParser, JsonParser
from config_file.utils import create_config_path, read_file, split_on_dot


class ConfigFile:
    def __init__(
        self,
        file_path: Type[Union[str, Type[PurePath]]],
        parser: Type[AbstractParser] = None,
    ) -> None:
        """
        Saves the config file path and expands it if needed, reads in
        the file contents, and determines what parser should be used for
        the given file.

        :param file_path: The path to your configuration file.
        :param parser: A custom parser you'd like used for your config file.

        :raises ValueError: If the specified file path does not have an extension
                            that is supported or it is a directory.
        """
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        self.__path = create_config_path(file_path)
        self.__contents = read_file(self.__path)
        self.__parser = self.__determine_parser(file_path, parser)

    @property
    def path(self) -> Type[PurePath]:
        return self.__path

    def __determine_parser(
        self, file_path: Type[PurePath], parser: Type[AbstractParser] = None
    ) -> Type[AbstractParser]:
        if parser is not None and not inspect.isabstract(parser):
            return parser(self.__contents)

        file_type = split_on_dot(file_path, only_last_dot=True)[-1]
        if file_type == "ini":
            return IniParser(self.__contents)
        elif file_type == "json":
            return JsonParser(self.__contents)
        else:
            raise ValueError(
                f"File path contains an unrecognized file type: {file_path}"
            )

    def get(
        self,
        key: str,
        parse_types: bool = False,
        return_type: Any = None,
        default: Any = None,
        all: bool = False,
    ) -> Any:
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

        :raises ValueError: If the value is not able to be coerced into return_type
        """
        if default is None:
            key_value = self.__parser.get(key, parse_types=parse_types)
        else:
            try:
                key_value = self.__parser.get(key, parse_types=parse_types)
            except ParsingError:
                return default

        return return_type(key_value) if return_type else key_value

    def set(self, key: str, value: Any) -> bool:
        """Sets the value of a key."""
        return self.__parser.set(key, value)

    def delete(self, section_key: str) -> bool:
        """Deletes a key/value pair or entire sections."""
        return self.__parser.delete(section_key)

    def stringify(self) -> str:
        """Convert the parsed internal representation of the file back into a string."""
        return self.__parser.stringify()

    def has(self, section_key: str) -> bool:
        """
        Check if a section, sub-section, or key exists in the file
        using a section.key format.

        Some formats, like JSON, do not have sections and therefore,
        it would only be checking if the key exists.
        """
        return self.__parser.has(section_key)

    def restore_original(
        self, original_file_path: Union[str, Type[PurePath]] = None
    ) -> bool:
        """
        Restores the original the config file by deleting it and copying the original
        back in its place. The internal contents of this config file object are then set
        to the newly reset config file.

        :param original_file_path: The path to the original config file to reset it to.
        If this is not provided and, say, your configuration file is config.json, the
        method would look for a config.original.json in the same folder by default.

        :return: True if the reset succeeded
        :raises FileNotFoundError: If the original configuration file does not exist
        :raises OSError: If self.path is not writable
        :raises SameFileError: If self.path and original_file_path are the same file.
        """
        if original_file_path is None:
            original_file_path = create_config_path(self.__path, original=True)

        if not Path(original_file_path).exists():
            raise FileNotFoundError(
                f"The {original_file_path} file to restore to does not exist."
            )

        self.__path.expanduser().unlink()
        copyfile(original_file_path, self.__path)
        self.__contents = read_file(self.__path)
        self.__parser.parsed_content = self.__parser.parse(self.__contents)

        return True

    def save(self) -> bool:
        """
        Save the configuration changes by writing the file out to the specified path
        :return: True if the save succeeded.
        """
        with open(self.__path, "w") as config_file:
            config_file.write(self.__parser.stringify())

        return True
