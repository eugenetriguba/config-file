from pathlib import Path
from typing import List, Union


def split_on_dot(line: Union[str, Path], only_last_dot=False) -> List[str]:
    """
    Split a string on the dot character (.).

    Args:
        line: The line ot split on.
        only_last_dot: Only split on the last occurrence of the dot.

    Raises:
        ValueError: if the line does not have a dot.
    """
    if isinstance(line, Path):
        line = str(line)

    if "." not in line:
        raise ValueError(f"The given string does not have a dot to split on: {line}")

    return line.rsplit(".", 1) if only_last_dot else line.split(".")


def read_file(path: Union[str, Path]) -> str:
    with open(path, "r") as file:
        return file.read()


def create_config_path(file_path: Path, original: bool = False) -> Path:
    if len(file_path.parts) >= 1 and file_path.parts[0] == "~":
        return file_path.expanduser()

    if original:
        file_parts = split_on_dot(file_path, only_last_dot=True)
        file_parts.insert(-1, "original")
        file_path = Path(".".join(file_parts))

    if file_path.is_dir():
        raise ValueError(f"The specified config file ({file_path}) is a directory.")

    return file_path


class Default:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Default Value: {} ({})".format(self.value, type(self.value))
