# def test_that_custom_parser_can_be_used(template_and_config_file):
#     class CustomParser(AbstractParser):
#         def __init__(self, file_contents):
#             super().__init__(file_contents)
#
#         def parse(self, file_contents: str):
#             return file_contents
#
#         def get(self, key, parse_types=True):
#             return key
#
#         def set(self, key, value):
#             return key, value
#
#         def delete(self, section_key):
#             return section_key
#
#         def has(self, section_key: str) -> bool:
#             return True
#
#         def stringify(self) -> str:
#             return str(self.parsed_content)
#
#     template_file, config = template_and_config_file(parser=CustomParser)
#
#     assert isinstance(config._ConfigFile__parser, CustomParser)
#     assert config.get("key") == "key"
#     assert config.set("key", "value") == ("key", "value")
#     assert config.delete("section_key") == "section_key"
#     assert config.has("blah")
#     assert config.stringify() == template_file.read_text()
