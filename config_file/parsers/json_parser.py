import json

from .base_parser import BaseParser


class JsonParser(BaseParser):
    def __init__(self, file_contents: str):
        super().__init__(
            file_contents=file_contents,
            module=json,
            decode_error=json.decoder.JSONDecodeError,
        )

    def stringify(self) -> str:
        return json.dumps(self.parsed_content, indent=4)
