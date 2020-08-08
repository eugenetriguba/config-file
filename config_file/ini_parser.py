import configparser

from .base_parser import BaseParser
from .ini_parser_compat import IniParserCompatibility


class IniParser(BaseParser):
    def __init__(self, file_contents: str):
        super().__init__(
            file_contents=file_contents,
            module=IniParserCompatibility,
            decode_error=configparser.Error,
        )
