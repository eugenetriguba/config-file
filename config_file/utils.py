from pathlib import Path
from typing import Union


def split_on_dot(line: Union[str, Path], only_last_dot=False):
    """
    Split a string on the dot character (.).

    :param line: The line ot split on.
    :param only_last_dot: Only split on the last occurrence of the dot.

    :raises ValueError: if the line does not have a dot.
    """
    if isinstance(line, Path):
        line = str(line)

    if "." not in line:
        raise ValueError(
            "The given string does not have a dot to split on: {}".format(line)
        )

    return line.rsplit(".", 1) if only_last_dot else line.split(".")


def read_file(path: Union[str, Path]):
    with open(path, "r") as file:
        return file.read()
