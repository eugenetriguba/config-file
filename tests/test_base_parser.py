import pytest

from config_file.parsers.base_parser import BaseParser


class ConcreteParser(BaseParser):
    def __init__(self, file_contents):
        super().__init__(file_contents)

    def get(self, key, parse_type=True):
        super().get(key, parse_type=parse_type)

    def set(self, key, value):
        super().set(key, value)

    def delete(self, section_key):
        super().delete(section_key)

    def has(self, section_key: str) -> bool:
        super().has(section_key)

    def stringify(self) -> str:
        super().stringify()

    def parse(self, file_contents: str):
        return file_contents


def test_that_base_parser_can_not_be_instantiated():
    with pytest.raises(TypeError):
        BaseParser("")


@pytest.mark.parametrize(
    "function, args",
    [
        (ConcreteParser("").get, ""),
        (ConcreteParser("").set, ("", "")),
        (ConcreteParser("").delete, ""),
        (ConcreteParser("").stringify, None),
        (ConcreteParser("").has, ""),
    ],
)
def test_that_base_parser_raises_not_implemented_errors(function, args):
    with pytest.raises(NotImplementedError):
        if args is None:
            function()
        elif type(args) is tuple:
            function(*args)
        else:
            function(args)
