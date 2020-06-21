from pathlib import Path, PurePath
from typing import Type, Union


def split_on_dot(line: Union[str, Type[PurePath]], only_last_dot=False) -> str:
    """
    Split a string on the dot character (.).

    :param line: The line ot split on.
    :param only_last_dot: Only split on the last occurrence of the dot.

    :raises ValueError: if the line does not have a dot.
    """
    if isinstance(line, PurePath):
        line = str(line)

    if "." not in line:
        raise ValueError(f"The given string does not have a dot to split on: {line}")

    return line.rsplit(".", 1) if only_last_dot else line.split(".")


def read_file(path: Union[str, Type[PurePath]]):
    with open(path, "r") as file:
        return file.read()


def create_config_path(file_path: Type[PurePath], original: bool = False) -> Path:
    if len(file_path.parts) >= 1 and file_path.parts[0] == "~":
        return file_path.expanduser()

    if original:
        file_parts = split_on_dot(file_path, only_last_dot=True)
        file_parts.insert(-1, "original")
        file_path = Path(".".join(file_parts))

    if file_path.is_dir():
        raise ValueError(f"The specified config file ({file_path}) is a directory.")

    return file_path
