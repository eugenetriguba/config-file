class ConfigFileError(Exception):
    """A generic error from the package."""


class MissingDependencyError(ConfigFileError):
    """
    yaml or toml dependencies were not installed,
    but the parsers for them were attempted to be used.
    """


class UnrecognizedFileError(ConfigFileError):
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
