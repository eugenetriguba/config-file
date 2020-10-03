from typing import Type

import pytest

from config_file.abstract_parser import AbstractParser
from config_file.base_parser import BaseParser


class ConcreteAbstractParser(AbstractParser):
    """
    ConcreteParser is a concrete implementation of the
    AbstractParser that just calls the AbstractParser's
    methods so we can ensure they raise a NotImplementedError.
    """

    def __init__(self, file_contents):
        super().__init__(file_contents)

    def get(self, key):
        super().get(key)

    def set(self, key, value):
        super().set(key, value)

    def delete(self, section_key):
        super().delete(section_key)

    def has(self, section_key: str, wild: bool = False):
        super().has(section_key)

    def stringify(self):
        super().stringify()

    def reset_internal_contents(self, file_contents: str) -> None:
        super().reset_internal_contents(file_contents)

    def parsed_content(self) -> dict:
        super().parsed_content()


def test_that_abstract_parser_can_not_be_instantiated():
    """
    config_file.abstract_parser.AbstractParser

    Ensure the AbstractParser raises a TypeError when it is
    instantiated.
    """
    with pytest.raises(TypeError):
        AbstractParser("")


def test_that_base_parser_can_not_be_instantiated():
    """
    config_file.base_parser.BaseParser

    Ensure the BaseParser raises a TypeError when it is
    instantiated.
    """
    with pytest.raises(TypeError):
        BaseParser("")


@pytest.mark.parametrize(
    "function, args",
    [
        (ConcreteAbstractParser("").get, ("",)),
        (ConcreteAbstractParser("").set, ("", "")),
        (ConcreteAbstractParser("").delete, ("",)),
        (ConcreteAbstractParser("").stringify, None),
        (ConcreteAbstractParser("").has, ("",)),
        (ConcreteAbstractParser("").reset_internal_contents, ("",)),
        (ConcreteAbstractParser("").parsed_content, None),
    ],
)
def test_that_abstract_and_base_parser_raises_not_implemented_errors(function, args):
    """
    config_file.abstract_parser.AbstractParser
    config_file.base_parser.BaseParser

    Ensure the AbstractParser and BaseParser raises a NotImplementedError
    for every method in it.
    """
    with pytest.raises(NotImplementedError):
        if args is None:
            function()
        else:
            function(*args)
