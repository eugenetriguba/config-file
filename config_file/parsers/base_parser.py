from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    The abstract base parser for all other parsers to implement.

    All the keys are specified in a 'dot' syntax. So if you have
    sections with subsections with a key that you're trying to get
    the value of, you'd use 'section.subsection.key' as the key parameter.
    """

    @abstractmethod
    def __init__(self, file_contents: str):
        """
        All parsers will take in the file as a string, parse
        them internally to their own representation that they
        can work with, and are able to stringify them back out
        when we need to save (write) them.

        It is up to the caller of the parser to read in the file to
        the parser and save the file when they are done using stringify().
        """
        self.__contents = self.__parse(file_contents)

    @abstractmethod
    def get(self, key, parse_type=True):
        """
        Retrieve the value of a key in its native type.
        This means the string 'true' will be parsed back as the
        boolean True.

        If parse_type is set to False, all values will be returned
        back as strings.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key, value):
        """Sets the value of a key."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key):
        """Deletes a key/value pair or entire sections."""
        raise NotImplementedError

    @abstractmethod
    def stringify(self) -> str:
        """
        Using self.__contents, converts the parsed internal representation
        of the file back into a string.
        """
        raise NotImplementedError

    @abstractmethod
    def has_section(self) -> bool:
        """Check if a section or sub-section in the file exists."""
        raise NotImplementedError

    @abstractmethod
    def has_key(self) -> bool:
        """Check if a key in the file exists."""

    @abstractmethod
    def __parse(self, file_contents: str):
        """
        Parse the file_contents into an internal representation
        the given parser can work with.
        """
        raise NotImplementedError


class ParsingError(Exception):
    """Unable to parse the configuration file"""
