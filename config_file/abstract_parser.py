from abc import ABC, abstractmethod
from typing import Any


class AbstractParser(ABC):
    """Abstract Parser is the API contract for a parser for
    use in the ConfigFile object.

    Every parser in ConfigFile implements this parser, and
    any user created parsers must implement this parser in
    order for this package to be able to use it.

    Every key is specified in a dot (.) syntax
    e.g. retrieving.some.deeply.nested.value

    If there is no dot in the key, it is assumed we are
    performing an action on a top level key, which could
    be an entire section.

    Args:
        file_contents: The stringified version of a file.
    """

    @abstractmethod
    def __init__(self, file_contents: str) -> None:
        self.file_contents = file_contents

    @property
    @abstractmethod
    def parsed_content(self) -> dict:
        """To be able to index into the ConfigFile object,
        we have to expose the parsed dictionary object.

        Raises:
            KeyError: If the key we are trying to index into
            does not exist.

        Returns:
            The internal contents parsed as a dictionary.
        """
        raise NotImplementedError

    @abstractmethod
    def reset_internal_contents(self, file_contents: str) -> None:
        """Reset the state of this parser to a new file.

        When restoring to the original file in ConfigFile,
        we need a way to reset the internal contents to this
        new file.

        While this may be as simple as setting the file_contents
        attribute value to the passed in file_contents argument,
        it likely would not be. This is because the initial
        passed in file contents would likely be parsed into some
        special form for the parser to work with more easily.

        Args:
            file_contents: The file contents of the new file.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieve the value of a key from the working file.

        Args:
            key: The key to retrieve.

        Returns:
            Whatever value the given key happens to contain.

        Raises:
            KeyError: If the key to retrieve does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set the value of a key in the working file.

        If the key does not exist, it should be created.

        Args:
            key: The key to set.
            value: The value to set the key to.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes a key from the working file.

        Args:
            key: The key we would like to remove.

        Raises:
            KeyError: If the key to remove does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def stringify(self) -> str:
        """Stringify the working file.

        Since the ConfigFile does not write out to disk
        after every operation, this method is what is
        used as the output for saving the file again.
        This parser should never write out to the disk.

        Returns:
            The file we are working with as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def has(self, key: str, wild: bool = False) -> bool:
        """Check whether the given key is in the parsed working file.

        This should not behave like a wild card, as in check
        if the key exists anywhere in the working file. Instead,
        if a key is given without a dot, it should be assumed we
        are checking the top level.

        Args:
            key: The key to search for.
            wild: Optionally search for any occurrence of key in the file.

        Returns:
            True if the working file has the key. False otherwise.
        """
        raise NotImplementedError
