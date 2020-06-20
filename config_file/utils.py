from pathlib import PurePath
from typing import Type, Union


def split_on_dot(line: Union[str, Type[PurePath]], only_last_dot=False):
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
