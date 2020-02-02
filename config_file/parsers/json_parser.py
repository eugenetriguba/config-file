import json

from nested_lookup import get_occurrence_of_key

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.parse_value import parse_value
from config_file.utils import split_on_dot


class JsonParser(BaseParser):
    def __init__(self, file_contents: str):
        """Reads in the file contents into the parser."""
        super().__init__(file_contents)

    def parse(self, file_contents: str):
        try:
            return json.loads(file_contents)
        except json.decoder.JSONDecodeError as error:
            raise ParsingError(error)

    def get(self, section_key, parse_type=True):
        split_keys = split_on_dot(section_key)

        result = self.parsed_content
        for key in split_keys:
            result = result[key]

        return parse_value(result) if parse_type else result

    def set(self, section_key, value):
        pass

    def delete(self, section_key):
        pass

    def stringify(self) -> str:
        return json.dumps(self.parsed_content)

    def has(self, search_key: str) -> bool:
        return get_occurrence_of_key(self.parsed_content, key=search_key) > 0
