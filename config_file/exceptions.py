class ConfigFileError(Exception):
    """A generic error from the package."""


class ParsingError(ConfigFileError):
    """Unable to parse the configuration file."""


class MissingDependencyError(ConfigFileError):
    """
    PyYaml or toml is not installed, but the parsers
    for them were attempted to be used.
    """


class UnrecognizedFileError(ConfigFileError):
    """
    A missing file extension or a file type not supported.
    """
