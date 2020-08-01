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
