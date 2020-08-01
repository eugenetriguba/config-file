import inspect
from pathlib import Path
from shutil import copyfile
from typing import Any, Optional, Type, Union

from config_file.exceptions import ParsingError, UnrecognizedFileError
from config_file.parsers.abstract_parser import AbstractParser
from config_file.parsers.ini_parser import IniParser
from config_file.parsers.json_parser import JsonParser
from config_file.parsers.parse_value import parse_value
from config_file.parsers.toml_parser import TomlParser
from config_file.parsers.yaml_parser import YamlParser
from config_file.utils import Default, create_config_path, read_file, split_on_dot


class ConfigFile:
    def __init__(
        self, file_path: Union[str, Path], parser: Optional[Type[AbstractParser]] = None
    ) -> None:
        """
        Stores the config file path and expands it if needed, reads in
        the file contents, and determines what parser should be used for
        the given file.

        Args:
            file_path: The path to your configuration file.
            parser: A custom parser you'd like used for your config file.

        Raises:
            ValueError: If the specified file path does not have an extension
                        that is supported or it is a directory.
        """
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        self.__path = create_config_path(file_path)
        self.__parser = self.__determine_parser(self.__path, parser)

    @property
    def path(self) -> Path:
        return self.__path

    def __determine_parser(
        self, file_path: Path, parser: Optional[Type[AbstractParser]] = None
    ) -> Type[AbstractParser]:
        file_contents = read_file(file_path)

        if parser is not None and not inspect.isabstract(parser):
            return parser(file_contents)

        try:
            file_type = split_on_dot(file_path, only_last_dot=True)[-1]
        except ValueError:
            raise UnrecognizedFileError(
                "Tried to determine a parser to use, but the file at "
                f"{file_path} does not have an extension."
            )

        return self.__find_parser_by_file_type(
            file_type=file_type, file_contents=file_contents, file_path=file_path
        )

    @staticmethod
    def __find_parser_by_file_type(
        file_type: str, file_path: Union[str, Path], file_contents: str
    ) -> Type[AbstractParser]:
        if file_type == "ini":
            return IniParser(file_contents)
        elif file_type == "json":
            return JsonParser(file_contents)
        elif file_type == "yaml" or file_type == "yml":
            return YamlParser(file_contents)
        elif file_type == "toml":
            return TomlParser(file_contents)
        else:
            raise UnrecognizedFileError(
                f"File path at `{file_path}` contains an unrecognized file type."
            )

    def get(
        self,
        key: str,
        parse_types: bool = False,
        return_type: Any = None,
        default: Any = Default(None),
    ) -> Any:
        """
        Retrieve the value of a key.

        Args:
            key: The key to retrieve.
            parse_types: Automatically parse ints, floats, booleans, dicts, and
                         lists. This recursively parses all types in whatever you're
                         retrieving, not just a single type.

                         e.g. If you are retrieving a section, all values in that
                         section will be parsed.

            return_type: The type to coerce the return value to.
            default: The default value to return if the value of the key is empty.

        Returns:
            The value of the key.

        Raises:
            ValueError: If the value is not able to be coerced into return_type.
        """
        try:
            key_value = self.__parser.get(key)
        except ParsingError as error:
            if default is not type(Default):
                key_value = default
            else:
                raise ParsingError(error)

        if parse_types:
            key_value = parse_value(key_value)

        return return_type(key_value) if return_type else key_value

    def set(self, key: str, value: Any) -> None:
        """Sets the value of a key.

        If the given key does not exist, it will be automatically
        created for you. That includes if there are multiple keys
        in a row that do not exist.
        e.g. set('exists.does_not.does_not.also_does_not', 5)

        The behavior of how this is done, however, depends on the
        file used. For example, with INI, subsections are not supported.
        So it would create a key in the section `exists` called `does_not`
        and set it to the value {'does_not': {'also_does_not': 5}}.

        Args:
            key: The section, sub-section, or key to delete.
            value: The value to set the key to.
        """
        self.__parser.set(key, value)

    def delete(self, key: str) -> None:
        """Deletes a section or key.

        Args:
            key: The section, sub-section, or key to delete.

        Raises:
            MissingKeyError: If a key is attempted to be deleted that
            does not exist.
        """
        self.__parser.delete(key)

    def stringify(self) -> str:
        """Retrieves file contents as a string.

        Returns:
            The internal representation of the file
            that has been read in converted to a string.
        """
        return self.__parser.stringify()

    def has(self, key: str, wild: bool = False) -> bool:
        """
        Check if a section, sub-section, or key exists.

        Some formats, like JSON, do not have sections and
        therefore, it would only be checking if a particular
        key exists.

        Args:
            key: The section, sub-section, or key to find.
            wild: Whether or not to search everywhere.

            Without `wild`, a single word `key` without a `.`
            will look at the outer most heirarchy of the file for it.

            With `wild`, that single word `key` will be searched
            for throughout the entire file.

        Returns:
            True if the key exists. False otherwise.
        """
        return self.__parser.has(key, wild=wild)

    def restore_original(
        self, original_file_path: Union[str, Path, None] = None
    ) -> None:
        """Restores the original the configuration file.

        The current one is deleted and the original is copied back
        in its place. The internal contents are then reset to the
        new file.

        Args:
            original_file_path: The original file to reset to.

            If this is not provided, it is calculated for you.
            e.g. if your configuration file is named config.json,
            this will look for aa config.original.json in the same
            directory.

        Raises:
            FileNotFoundError: If the original configuration file (whether
            calculated or passed in) does not exist.

            OSError: If the current configuration path is not writable.

            SameFileError: If current configuration path and the passed in
            original_file_path are the same file.
        """
        if original_file_path is None:
            original_file_path = create_config_path(self.__path, original=True)

        if not Path(original_file_path).exists():
            raise FileNotFoundError(
                f"The {original_file_path} file to restore to does not exist."
            )

        self.__path.expanduser().unlink()
        copyfile(original_file_path, self.__path)
        self.__parser.reset_internal_contents(read_file(self.__path))

    def save(self) -> None:
        """
        Save your configuration changes.

        This writes the file back out, including any changes
        you've made, to the specified path given from this
        object's constructor.
        """
        with open(str(self.__path), "w") as config_file:
            config_file.write(self.stringify())
