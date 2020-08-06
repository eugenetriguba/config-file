from types import ModuleType
from typing import Any, Type

from config_file.abstract_parser import AbstractParser
from config_file.exceptions import ParsingError
from config_file.nested_lookup import get_occurrence_of_key
from config_file.utils import split_on_dot


class BaseParser(AbstractParser):
    def __init__(
        self, file_contents: str, module: ModuleType, decode_error: Type[Exception]
    ):
        """The BaseParser implements the AbstractParser for us by giving it any module.

        As long as the module has a `loads` and `dumps` method, the BaseParser can use
        it. Every file is then represented and worked with as a dictionary.

        Args:
            file_contents: The contents of the file to parse.

            module: The module to use to parse the files.
            Must have a `loads` and `dumps` method.

            decode_error: The error the module raises when the
            file cannot be decoded.

        Raises:
            ParsingError: If the decode_error is raised.
        """
        super().__init__(file_contents)
        self.__module = module
        self.__decode_error = decode_error
        self.parsed_content = self.parse_file_contents(module, decode_error)

    def parse_file_contents(self, module: ModuleType, decode_error: Exception) -> dict:
        """Parse the file contents by running the `loads`  method on the module.

        Args:
            module: The module to use to parse the file.
            decode_error: The error that is raised from the module if the file
            cannot be decoded.

        Raises:
            ParsingError: If the decode_error is raised while running `loads`.

        Returns:
            The parsed file as a dictionary.
        """
        try:
            return module.loads(self.file_contents)
        except decode_error as error:
            raise ParsingError(error)

    def reset_internal_contents(self, file_contents: str) -> None:
        """Reset the file contents and parsed contents of the parser.

        Args:
            file_contents: The new file contents.

        Raises:
            ParsingError: If we're unable to parse the new file contents.
        """
        self.file_contents = file_contents
        self.parsed_content = self.parse_file_contents(
            self.__module, self.__decode_error
        )

    def get(self, search_key: str) -> Any:
        key_causing_error = None

        try:
            if "." not in search_key:
                key_causing_error = search_key
                return self.parsed_content[search_key]
            else:
                split_keys = split_on_dot(search_key)

            content_reference = self.parsed_content
            for key in split_keys:
                key_causing_error = key
                content_reference = content_reference[key]

        except (KeyError, TypeError):
            raise KeyError(
                f"cannot `get` {search_key} because "
                f"{key_causing_error} is not subscriptable."
            )

        return content_reference

    def set(self, key: str, value: Any) -> None:
        if "." not in key:
            self.parsed_content[key] = value
            return

        keys = split_on_dot(key)
        content_reference = self.parsed_content
        for index, key in enumerate(keys):
            if index == len(keys) - 1:
                content_reference[key] = value
                return

            try:
                content_reference = content_reference[key]
            except KeyError:
                content_reference[key] = {}
                content_reference = content_reference[key]

    def delete(self, key: str) -> None:
        try:
            if "." not in key:
                del self.parsed_content[key]
            else:
                indexes = split_on_dot(key)
                indexes_length = len(indexes)

                content_reference = self.parsed_content
                for index, key in enumerate(indexes):
                    if index == indexes_length - 1:
                        del content_reference[key]
                        break

                    content_reference = content_reference[key]
        except (KeyError, TypeError):
            raise KeyError(f"The specified key '{key}' to delete was not found.")

    def stringify(self) -> str:
        return self.__module.dumps(self.parsed_content)

    def has(self, search_key: str, wild: bool = False) -> bool:
        if wild:
            return get_occurrence_of_key(self.parsed_content, key=search_key) > 0

        try:
            self.get(search_key)
            return True
        except (KeyError, ParsingError):
            return False
