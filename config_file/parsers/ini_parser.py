import configparser
from io import StringIO

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.parse_value import parse_value
from config_file.utils import split_on_dot


class IniParser(BaseParser):
    def __init__(self, file_contents: str):
        """Reads in the file contents into the configparser."""
        super().__init__(file_contents)

    def parse(self, file_contents: str):
        try:
            parser = configparser.ConfigParser()
            parser.read_string(file_contents)
            return parser
        except configparser.Error as error:
            raise ParsingError(error)

    def get(self, section_key: str, parse_types: bool = False):
        """
        Read the value of `section.key` of the config file.

        :param section_key: The section and key to read from in the config file.
        e.g. 'section1.key2'
        :param parse_types: Coerces the return value to its native type.
        :return: The value of the key, parsed to its native type if parse_types is True.

        :raises ValueError: if the section_key given is not in a dot format. e.g.
                            'section1.key'
        :raises ParsingError: if the specified `section.key` is not found, in an
        invalid format, or if we are unable to coerce the return value to value_type.
        """
        if "." not in section_key:
            return self.__retrieve_section(section_key, parse_types)

        try:
            section, key = split_on_dot(section_key, only_last_dot=True)
            value = self.parsed_content.get(section, key)
            return parse_value(value) if parse_types else value
        except configparser.Error as error:
            raise ParsingError(error.message)

    def __retrieve_section(self, section, parse_types):
        items = dict(self.parsed_content.items(section))

        if not parse_types:
            return items

        for item in items:
            items[item] = parse_value(items[item])

        return items

    def set(self, section_key: str, value) -> bool:
        """
        Sets the value of 'section.key' of the config file. If the specified section
        is not in the configuration file, it will be created before adding the key
        to it.

        :param section_key: The key to set from the config file. e.g. 'section1.key'

        :param value: The value to set the key to. It can be any type that can
                      be converted to a string.

        :return: True if the setting was successful.

        :raises ValueError: If there is no dot (.) in section_key
        """
        section, key = split_on_dot(section_key, only_last_dot=True)

        if value is not None and not self.parsed_content.has_section(section):
            self.parsed_content.add_section(section)

        if not isinstance(value, str):
            value = str(value)

        self.parsed_content.set(section, key, value)
        return True

    def delete(self, section_key: str) -> bool:
        """
        Deletes a key or an entire section.

        :param section_key: The key to delete from the config file.
        e.g. 'ocr.engine'. If no dot (.) is present, it will assume you are trying
        to delete the entire section.

        :return: True if the deletion succeeded.

        :raise ValueError: If the section or key does not exist in the config file.
        """
        if "." not in section_key:
            if not self.parsed_content.has_section(section_key):
                raise ValueError(
                    f"Cannot delete {section_key} because it is not in the config file."
                )

            self.parsed_content.remove_section(section_key)
            return True

        section, key = split_on_dot(section_key, only_last_dot=True)
        if key not in self.parsed_content[section]:
            raise ValueError(
                f"Cannot delete {section}.{key} because {key} is not in {section}."
            )

        self.parsed_content.remove_option(section, key)
        return True

    def stringify(self) -> str:
        buffer = StringIO()
        self.parsed_content.write(buffer)
        return buffer.getvalue()

    def has(self, section_key: str) -> bool:
        if "." not in section_key:
            return self.parsed_content.has_section(section_key)

        section, key = split_on_dot(section_key, only_last_dot=True)
        return self.parsed_content.has_option(section, key)
