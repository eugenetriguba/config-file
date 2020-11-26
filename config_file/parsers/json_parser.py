import json
from typing import Type

from .base_parser import BaseParser


class JsonParser(BaseParser):
    def __init__(self, file_contents: str):
        super().__init__(file_contents)

    @property
    def decode_error(self) -> Type[Exception]:
        return json.decoder.JSONDecodeError

    def loads(self, contents: str) -> dict:
        return json.loads(contents)

    def dumps(self, loaded_contents: dict) -> str:
        return json.dumps(loaded_contents, indent=4)
