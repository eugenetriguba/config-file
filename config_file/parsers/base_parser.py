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
        self.contents = file_contents
        self.parsed_content = self.parse(self.contents)

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
    def delete(self, section_key):
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
    def has(self, section_key: str) -> bool:
        """
        Check if a section, sub-section, or key exists in the file
        using a section.key format.

        Some formats, like JSON, do not have sections and therefore,
        it would only be checking if
        """
        raise NotImplementedError

    @abstractmethod
    def parse(self, file_contents: str):
        """
        Parse the file_contents into an internal representation
        the given parser can work with. It should not return anything
        if you're going to be using the super() constructor.
        """
        raise NotImplementedError


class ParsingError(Exception):
    """Unable to parse the configuration file"""
