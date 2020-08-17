import configparser
from io import StringIO
from typing import Type

from .base_parser import BaseParser


class IniParser(BaseParser):
    def __init__(self, file_contents: str):
        super().__init__(file_contents)

    @property
    def decode_error(self) -> Type[Exception]:
        return configparser.Error

    def loads(self, contents: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read_string(contents)

        return self.__create_configparser_dict(parser)

    def dumps(self, loaded_contents: dict) -> str:
        parser = configparser.ConfigParser()
        buffer = StringIO()

        parser.read_dict(loaded_contents)
        parser.write(buffer)

        return buffer.getvalue()

    def __create_configparser_dict(self, parser: configparser.ConfigParser) -> dict:
        result = {}
        items = dict(parser.items())

        for section in parser.sections():
            result.update({str(section): dict(items[section])})

        return result
