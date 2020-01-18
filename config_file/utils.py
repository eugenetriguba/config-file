def split_on_dot(line: str, only_last_dot=False):
    """
    Split a string on the dot character (.).

    :param line: The line ot split on.
    :param only_last_dot: Only split on the last occurrence of the dot.

    :raises ValueError: if the line does not have a dot.
    """
    if "." not in line:
        raise ValueError(
            "section_key must contain the section and key separated by a dot. "
            + "e.g. 'section.key'"
        )

    return line.rsplit(".", 1) if only_last_dot else line.split(".")
