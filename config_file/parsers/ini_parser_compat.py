import configparser
from io import StringIO


class IniParserCompatibility:
    """
    Provides compatibility with the json, yaml,
    and toml API so we can use the BaseParser
    easily, while still being able to leverage
    the built-in configparser to parse the file.

    It is used as the `module` parameter
    for BaseParser, which requires us to have a
    `dumps` and `loads` method.
    """

    @staticmethod
    def loads(file_contents: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read_string(file_contents)

        return IniParserCompatibility.__create_configparser_dict(parser)

    @staticmethod
    def dumps(file_contents: dict) -> str:
        parser = configparser.ConfigParser()
        buffer = StringIO()

        parser.read_dict(file_contents)
        parser.write(buffer)

        return buffer.getvalue()

    @staticmethod
    def __create_configparser_dict(parser: configparser.ConfigParser) -> dict:
        result = {}
        items = dict(parser.items())

        for section in parser.sections():
            result.update({str(section): dict(items[section])})

        return result
