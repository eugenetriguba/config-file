from pathlib import Path
from typing import List, Union


def split_on_dot(line: Union[str, Path], only_last_dot: bool = False) -> List[str]:
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


class Default:
    """
    Default is used for the `default` value in ConfigFile's `get`.

    Previously, the default value for `get` was None. However, then
    the user cannot have `get` return a default value of None. So this
    class is used instead to get around that limitation.
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Default Value: {} ({})".format(self.value, type(self.value))
