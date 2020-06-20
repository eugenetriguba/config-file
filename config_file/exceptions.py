class ConfigFileError(Exception):
    """A generic error from the package."""

class ParsingError(ConfigFileError):
    """Unable to parse the configuration file."""
    