import pytest

from config_file.abstract_parser import AbstractParser


class ConcreteParser(AbstractParser):
    def __init__(self, file_contents):
        super().__init__(file_contents)

    def get(self, key):
        super().get(key)

    def set(self, key, value):
        super().set(key, value)

    def delete(self, section_key):
        super().delete(section_key)

    def has(self, section_key: str):
        super().has(section_key)

    def stringify(self):
        super().stringify()

    def reset_internal_contents(self, file_contents: str) -> None:
        super().reset_internal_contents(file_contents)


def test_that_abstract_parser_can_not_be_instantiated():
    with pytest.raises(TypeError):
        AbstractParser("")


@pytest.mark.parametrize(
    "function, args",
    [
        (ConcreteParser("").get, ("",)),
        (ConcreteParser("").set, ("", "")),
        (ConcreteParser("").delete, ("",)),
        (ConcreteParser("").stringify, None),
        (ConcreteParser("").has, ("",)),
        (ConcreteParser("").reset_internal_contents, ("",)),
    ],
)
def test_that_abstract_parser_raises_not_implemented_errors(function, args):
    with pytest.raises(NotImplementedError):
        if args is None:
            function()
        else:
            function(*args)
