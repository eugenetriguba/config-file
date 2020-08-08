from pathlib import Path

import pytest

from config_file.utils import Default, split_on_dot


def test_that_split_on_dot_splits_the_line_correctly():
    """
    config_file.utils.split_on_dot

    Ensure splitting a string with dots in it returns an
    array of strings split on those dots.
    """
    assert split_on_dot("section.key.blah") == ["section", "key", "blah"]


def test_that_split_on_dot_can_only_split_on_the_last_one():
    """
    config_file.utils.split_on_dot

    Ensure that the only_last_dot parameter only splits the input
    on the last dot.
    """
    assert split_on_dot("test.input.should.only.split.on.last", only_last_dot=True) == [
        "test.input.should.only.split.on",
        "last",
    ]


def test_that_split_on_dot_raises_error_when_there_is_no_dot():
    """
    config_file.utils.split_on_dot

    Ensure that a ValueError is raised if the input to split_on_dot
    has no dot (.) in it.
    """
    with pytest.raises(ValueError):
        split_on_dot("this line has no dots in it")


def test_that_split_on_dot_can_accept_path_objects():
    """
    config_file.utils.split_on_dot

    Ensure that a pathlib.Path object is able to be
    given to split_on_dot.
    """
    split = split_on_dot(Path("some.file.path.with.dots"))

    assert split == ["some", "file", "path", "with", "dots"]


def test_that_default_is_initialized_correctly():
    """
    config_file.utils.Default

    Ensure that the Default class's value attribute
    is the same value that it was constructed with.
    """
    default = Default(5)
    assert default.value == 5


def test_that_default_has_the_correct_repr_format():
    """
    config_file.utils.Default

    Ensure that when the Default class is coerced to
    a string, it has the correct format and output.
    """
    default = Default("test")
    assert str(default) == "Default Value: test (<class 'str'>)"
