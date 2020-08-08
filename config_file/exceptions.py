class ParsingError(ValueError):
    """
    Unable to parse the configuration file.

    Since every module that parses the different
    files has it's own decode error, this standardizes
    it for the package to only raise a ParsingError
    if a error occurs in those instances.
    """
