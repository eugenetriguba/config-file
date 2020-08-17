from abc import abstractmethod
from typing import Any, Type

from config_file.abstract_parser import AbstractParser
from config_file.exceptions import ParsingError
from config_file.nested_lookup import get_occurrence_of_key
from config_file.utils import split_on_dot


class BaseParser(AbstractParser):
    def __init__(self, file_contents: str):
        """The BaseParser implements the AbstractParser for us, as long as the
        subclasses implement `loads`, `dumps`, and `decode_error` methods.

        Internally, every parser uses the BaseParser so it does not
        have to re-implement common dictionary manipulation logic. However,
        there is nothing about the BaseParser that is a requirement for
        using ConfigFile.

        Args:
            file_contents: The contents of the file to parse.

        Raises:
            ParsingError: If the decode_error is raised.
        """
        super().__init__(file_contents)
        self.__parsed_content = self.parse_file_contents()

    @abstractmethod
    def loads(self, contents: str) -> dict:
        """Transforms the file contents into a dictionary.

        Args:
            contents: The file contents to transform.

        Raises:
            self.decode_error: If there is a decoding error
            while attempting to parse the string.

        Returns:
            The contents of a particular file as a dictionary
            we can manipulate.
        """
        raise NotImplementedError

    @abstractmethod
    def dumps(self, loaded_contents: dict) -> str:
        """Transform the parsed contents back into a string.

        Args:
            loaded_contents: The file contents from a self.loads call.

            It doesn't necessary need to be from a loads call, could just
            be a valid dictionary for the given format, but that is the
            typical usecase.

        Raises:
            self.decode_error: If there is a decoding error
            while attempting to transform the dict back into a string.

        Returns:
            The dictionary parsed back into a string.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def decode_error(self) -> Type[Exception]:
        """The decoding error raised by the subclass on loads/dumps.

        Returns:
            The decoding error
        """
        raise NotImplementedError

    @property
    def parsed_content(self) -> dict:
        return self.__parsed_content

    def parse_file_contents(self) -> dict:
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
            return self.loads(self.file_contents)
        except self.decode_error as error:
            raise ParsingError(error)

    def reset_internal_contents(self, file_contents: str) -> None:
        """Reset the file contents and parsed contents of the parser.

        Args:
            file_contents: The new file contents.

        Raises:
            ParsingError: If we're unable to parse the new file contents.
        """
        self.file_contents = file_contents
        self.__parsed_content = self.parse_file_contents()

    def get(self, search_key: str) -> Any:
        key_causing_error = None

        try:
            if "." not in search_key:
                key_causing_error = search_key
                return self.__parsed_content[search_key]
            else:
                split_keys = split_on_dot(search_key)

            content_reference = self.__parsed_content
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
            self.__parsed_content[key] = value
            return

        keys = split_on_dot(key)
        content_reference = self.__parsed_content
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
                del self.__parsed_content[key]
            else:
                indexes = split_on_dot(key)
                indexes_length = len(indexes)

                content_reference = self.__parsed_content
                for index, key in enumerate(indexes):
                    if index == indexes_length - 1:
                        del content_reference[key]
                        break

                    content_reference = content_reference[key]
        except (KeyError, TypeError):
            raise KeyError(f"The specified key '{key}' to delete was not found.")

    def stringify(self) -> str:
        return self.dumps(self.__parsed_content)

    def has(self, search_key: str, wild: bool = False) -> bool:
        if wild:
            return get_occurrence_of_key(self.__parsed_content, key=search_key) > 0

        try:
            self.get(search_key)
            return True
        except (KeyError, ParsingError):
            return False
