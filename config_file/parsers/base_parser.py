from types import ModuleType
from typing import Any

from config_file.exceptions import MissingKeyError, ParsingError
from config_file.nested_lookup import get_occurrence_of_key
from config_file.utils import split_on_dot

from .abstract_parser import AbstractParser


class BaseParser(AbstractParser):
    def __init__(self, file_contents: str, module: ModuleType, decode_error: Exception):
        super().__init__(file_contents)
        self.__module = module
        self.__decode_error = decode_error
        self.parsed_content = self.parse_file_contents(module, decode_error)

    def parse_file_contents(self, module, decode_error) -> Any:
        try:
            return module.loads(self.file_contents)
        except decode_error as error:
            raise ParsingError(error)

    def reset_internal_contents(self, file_contents: str) -> None:
        self.file_contents = file_contents
        self.parsed_content = self.parse_file_contents(
            self.__module, self.__decode_error
        )

    def get(self, search_key: str) -> Any:
        if "." not in search_key:
            result = self.parsed_content[search_key]
            return result
        else:
            split_keys = split_on_dot(search_key)

        result = self.parsed_content
        key_causing_error = None
        try:
            for key in split_keys:
                key_causing_error = key
                result = result[key]
        except (KeyError, TypeError):
            raise ParsingError(
                f"Cannot `get` {search_key} because "
                f"{key_causing_error} is not subscriptable."
            )

        return result

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
            raise MissingKeyError(f"The specified key '{key}' to delete was not found.")

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
