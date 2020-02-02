import json

from nested_lookup import (
    get_occurrence_of_key,
    nested_delete,
    nested_lookup,
    nested_update,
)

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.parse_value import parse_value
from config_file.utils import split_on_dot


class JsonParser(BaseParser):
    """
    The JsonParser allows use of json files with ConfigFile. The syntax it
    supports is a bit more flexible than the IniParser.

    Since you can have deeply nested structures with JSON, the JsonParser supports
    a catch all where you can get/set/delete all occurrences of a particular
    key. This is the default behavior if you only specify a single word key.

    If there is a '.' in the key, it is assumed you want to use the dot syntax
    then.

    If no '.' is in the key parameter and we have specified we're only
    trying to fetch a top level item with 'top_level_only=True', the parser
    only retrieve the key in the top most level.

    Example:

        >>> json = {
        >>>    "key1": {
        >>>        "key2": "foo",
        >>>        "key1": "bar"
        >>>    },
        >>>    "foo": "bar"
        >>> }
        >>> parser = JsonParser(json.dumps(json))
        >>> parser.get('key1')
        { "key2": "foo", "key1": "bar" }
        >>> parser.get('key1.key2')
        "foo"
        >>> parser.get('key1', retrieve_all=True)
        [{ "key2": "foo", "key1": "bar" }, "bar"]
    """

    def __init__(self, file_contents: str):
        """Reads in the file contents into the parser."""
        super().__init__(file_contents)

    def parse(self, file_contents: str):
        try:
            return json.loads(file_contents)
        except json.decoder.JSONDecodeError as error:
            raise ParsingError(error)

    def get(self, key: str, parse_type: bool = True, retrieve_all: bool = False):
        """
        Retrieve values using a dot syntax.

        :param key: The key to retrieve. e.g. 'foo.bar.boo'

        :param parse_type: Whether you'd like the type parsed into its native one.

        :param retrieve_all: Specify whether you'd like to recursively receive
        all values that match the given key. Returned as a list.
        e.g. 'foo' would retrieve all values that have the key 'foo', anywhere
        in the json.

        :return: the value of the given key
        """
        if retrieve_all:
            result = nested_lookup(key, self.parsed_content)
        elif "." in key:
            split_keys = split_on_dot(key)
            result = self.parsed_content
            for key in split_keys:
                result = result[key]
        else:
            result = self.parsed_content[key]

        return parse_value(result) if parse_type else result

    def set(self, key: str, value, set_all: bool = False):
        if set_all:
            nested_update(self.parsed_content, key, value, in_place=True)
        elif "." in key:
            indexes = split_on_dot(key)
            indexes_length = len(indexes)

            ref = self.parsed_content
            for index, key in enumerate(indexes):
                if index == indexes_length - 1:
                    ref[key] = value
                    break

                ref = ref[key]
        else:
            self.parsed_content[key] = value

        return True

    def delete(self, key, delete_all: bool = False):
        if delete_all:
            nested_delete(self.parsed_content, key, in_place=True)
        elif "." in key:
            indexes = split_on_dot(key)
            indexes_length = len(indexes)

            ref = self.parsed_content
            for index, key in enumerate(indexes):
                if index == indexes_length - 1:
                    del ref[key]
                    break

                ref = ref[key]
        else:
            del self.parsed_content[key]

        return True

    def stringify(self) -> str:
        return json.dumps(self.parsed_content)

    def has(self, search_key: str) -> bool:
        return get_occurrence_of_key(self.parsed_content, key=search_key) > 0
