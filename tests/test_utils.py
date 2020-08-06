import pytest

from config_file.utils import Default, split_on_dot


@pytest.mark.parametrize(
    "test_input, only_last_dot, expected_result",
    [("section.key.blah", False, ["section", "key", "blah"])],
)
def test_that_split_on_dot_splits_the_line_correctly(
    test_input, only_last_dot, expected_result
):
    assert split_on_dot(test_input, only_last_dot=only_last_dot) == expected_result


@pytest.mark.parametrize("test_input", ["this line has no dots in it"])
def test_that_split_on_dot_raises_error_when_there_is_no_dot(test_input):
    with pytest.raises(ValueError):
        split_on_dot(test_input)


def test_that_default_is_initialized_correctly():
    default = Default(5)
    assert default.value == 5


def test_that_default_has_the_correct_repr_format():
    default = Default("test")
    assert str(default) == "Default Value: test (<class 'str'>)"
