import configparser
from io import StringIO

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.parse_value import parse_value


class IniParser(BaseParser):

    def __init__(self, file_contents: str):
        """Reads in the file contents into the parser."""
        try:
            self.parser = configparser.ConfigParser()
            super().__init__(file_contents)
        except configparser.Error as error:
            raise ParsingError(error)

    def parse(self, file_contents: str):
        self.parser.read_string(file_contents)

    def get(self, section_key, parse_type=True):
        """
        Read the value of `section.key` of the config file.

        :param section_key: The section and key to read from in the config file.
        e.g. 'section1.key2'
        :param parse_type: Coerces the return value to its native type.
        :return: The value of the key, parsed to its native type if parse_type is True.

        :raises ValueError: if the section_key given is not in a dot format. e.g. 'section1.key'
        :raises ParsingError: if the specified `section.key` is not found, in an
        invalid format, or if we are unable to coerce the return value to value_type.
        """
        section, key = self._split_on_dot(section_key)

        try:
            value = self.parser.get(section, key)
            return parse_value(value) if parse_type else value
        except configparser.Error as error:
            raise ParsingError(error.message)

    def set(self, section_key, value):
        """
        Sets the value of 'section.key' of the config file. If the specified section
        is not in the configuration file, it will be created before adding the key
        to it.

        :param section_key: The key to set from the config file. e.g. 'section1.key'
        :param value: The value to set the key to.

        :return: True if the setting was successful.
        :rtype: boolean

        :raises ValueError: If there is no dot (.) in section_key
        """
        section, key = self._split_on_dot(section_key)

        if value is not None and not self.parser.has_section(section):
            self.parser.add_section(section)

        self.parser.set(section, key, value)
        return True

    def delete(self, section_key):
        """
        Deletes a key or an entire section.

        :param section_key: The key to delete from the config file.
        e.g. 'ocr.engine'. If no dot (.) is present, it will assume you are trying
        to delete the entire section.

        :return: True if the deletion succeeded.
        :rtype: boolean

        :raise ValueError: If the section or key does not exist in the config file.
        """
        if "." not in section_key:
            if not self.parser.has_section(section_key):
                raise ValueError(
                    f"Cannot delete {section_key} because it is not in the config file."
                )

            self.parser.remove_section(section_key)
            return True

        section, key = self._split_on_dot(section_key)
        if key not in self.parser[section]:
            raise ValueError(
                f"Cannot delete {section}.{key} because {key} is not in {section}."
            )

        self.parser.remove_option(section, key)
        return True

    def stringify(self) -> str:
        buffer = StringIO()
        self.parser.write(buffer)
        return buffer.getvalue()

    def has(self, section_key: str) -> bool:
        if "." not in section_key:
            return self.parser.has_section(section_key)

        section, key = self._split_on_dot(section_key)
        return self.parser.has_option(section, key)
