class ConfigFileError(Exception):
    """A generic error from the package."""


class UnsupportedFileTypeError(ConfigFileError):
    """
    A missing file extension or a file type not supported.
    """


class ParsingError(ConfigFileError):
    """Unable to parse the configuration file."""


class MissingKeyError(ParsingError):
    """
    A key that was specified (to retrieve, delete, etc.)
    is not in the file.
    """
