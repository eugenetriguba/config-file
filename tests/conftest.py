from pathlib import Path
from typing import Callable, Tuple, Type, Union

import pytest

from config_file.abstract_parser import AbstractParser
from config_file.config_file_path import ConfigFilePath


@pytest.fixture
def tmp_file(tmp_path) -> Callable[[str, str], Path]:
    """
    Retrieve the path to a a temporary file.

    Args:
        file_name: The name of the file to create.
        file_contents: The contents of the temporary file.

    Returns:
        A Path pointing at the temporary file that has been created.
    """

    def func(file_name: str, file_contents: str) -> Path:
        file = tmp_path / file_name
        file.touch()
        file.write_text(file_contents, encoding="utf-8")
        return file

    return func


@pytest.fixture
def template_file(tmp_file: Callable[[str, str], Path]) -> Callable[[str, str], Path]:
    """
    Retrieve a path to a file from the test templates/

    All these files mirror each other for every file type
    so that one test can run on all the different file types.

    Args:
        file_type: The filetype to retrieve i.e. "ini"
        template_name: The name of the template to retrieve.
            Defaults to the "default" template. i.e. the template
            with the name "default" with it's respective file extension.
    
    Returns:
        A Path object point to that test template.
    """
    template_dir = Path(__file__).parent / "templates"

    def func(file_type: str, template_name: str = "default") -> Path:
        file_name = f"{template_name}.{file_type}"
        template = template_dir / file_type / file_name

        return tmp_file(file_name, template.read_text(encoding="utf-8"))

    return func


@pytest.fixture
def template_original_file() -> Callable[[Path], Path]:
    """
    Retrieve the "original" version of a template test file.

    None of the "original" files are actually stored in templates/.
    Instead, it is created on the fly with the same contents. The
    purpose here is that some functionality requires a filename.original.ext
    name, namely, restore_original().

    Args:
        template_path: The path to the temporary template file we're using.
    
    Returns:
        A Path object pointing to the newly created original template file.
    """

    def func(template_path: Union[str, Path]):
        if isinstance(template_path, str):
            template_path = Path(template_path)

        original_path = ConfigFilePath(template_path).original_path
        original_path.touch()
        original_path.write_text(template_path.read_text(encoding="utf-8"))

        return original_path

    return func


@pytest.fixture
def template_and_parser(
    template_file: Callable[[str, str], Path]
) -> Callable[[str, str], Tuple[Path, Type[AbstractParser]]]:
    """
    Retrieve the parser and test template for a particular
    supported file type.

    Args:
        file_type: The parser type to retrieve i.e. "ini" -> IniParser
        template_name: The template to retrieve. Defaults to the
            "default" template file for each extension.
    
    Returns:
        The template and parser corresponding to the file_type with 
        the template file read in.
    """

    def func(
        file_type: str, template_name: str = "default"
    ) -> Tuple[Path, Type[AbstractParser]]:
        test_file = template_file(file_type, template_name)
        return test_file, ConfigFilePath(test_file).parser

    return func


@pytest.fixture
def templated_parser(template_and_parser) -> Callable[[str, str], Type[AbstractParser]]:
    """
    Retrieve a parser for a particular supported file type with
    a test template already read into it. Small helper around
    template_and_parser that only returns the parser.

    Args:
        file_type: The parser type to retrieve i.e. "ini" -> IniParser
        template_name: The template to retrieve. Defaults to the
            "default" template file for each extension.
    
    Returns:
        The parser corresponding to the file_type with the template file
        read in.
    """

    def func(file_type: str, template_name: str = "default") -> Type[AbstractParser]:
        return template_and_parser(file_type, template_name)[1]

    return func
