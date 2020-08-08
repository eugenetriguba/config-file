from pathlib import Path
from typing import Callable, Tuple, Type, Union

import pytest

from config_file import ConfigFile
from config_file.abstract_parser import AbstractParser
from config_file.config_file_path import ConfigFilePath


@pytest.fixture
def tmp_file(tmp_path) -> Callable[[str, str], Path]:
    def func(file_name: str, file_contents: str) -> Path:
        file = tmp_path / file_name
        file.touch()
        file.write_text(file_contents, encoding="utf-8")
        return file

    return func


@pytest.fixture
def template_file(tmp_file: Callable[[str, str], Path]) -> Callable[[str, str], Path]:
    template_dir = Path(__file__).parent / "templates"

    def func(file_type: str, template_name: str = "default") -> Path:
        file_name = f"{template_name}.{file_type}"
        template = template_dir / file_type / file_name

        return tmp_file(file_name, template.read_text(encoding="utf-8"))

    return func


@pytest.fixture
def template_original_file() -> Callable[[Path], Path]:
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
    def func(
        file_type: str, template_name: str = "default"
    ) -> Tuple[Path, Type[AbstractParser]]:
        test_file = template_file(file_type, template_name)
        return test_file, ConfigFile(test_file)._ConfigFile__parser

    return func


@pytest.fixture
def templated_parser(template_and_parser) -> Callable[[str, str], Type[AbstractParser]]:
    def func(file_type: str, template_name: str = "default") -> Type[AbstractParser]:
        return template_and_parser(file_type, template_name)[1]

    return func
