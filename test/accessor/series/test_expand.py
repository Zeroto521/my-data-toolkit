import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.series import expand  # noqa: F401


@pytest.mark.parametrize(
    "suffix, delimiter, flatten, data, name, expected",
    [
        # test default parameters
        (
            None,
            "_",
            False,
            [(1, 2), (3, 4)],
            "item",
            {
                "item_0": [1, 3],
                "item_1": [2, 4],
            },
        ),
        # test delimiter
        (
            None,
            "-",
            False,
            [(1, 2), (3, 4)],
            "item",
            {
                "item-0": [1, 3],
                "item-1": [2, 4],
            },
        ),
        # test suffix
        (
            ["a", "b"],
            "_",
            False,
            [(1, 2), (3, 4)],
            "item",
            {
                "item_a": [1, 3],
                "item_b": [2, 4],
            },
        ),
        # test len(suffix) > max length of elements
        (
            ["a", "b", "c"],
            "_",
            False,
            [(1, 2), (3, 4)],
            "item",
            {
                "item_a": [1, 3],
                "item_b": [2, 4],
            },
        ),
        # test each element length is different
        (
            None,
            "_",
            False,
            [(1, 2), (3, 4, 5)],
            "item",
            {
                "item_0": [1, 3],
                "item_1": [2, 4],
                "item_2": [np.nan, 5],
            },
        ),
        # test len(suffix) > max length of elements
        (
            ["a", "b", "c", "d"],
            "_",
            False,
            [(1, 2), (3, 4, 5)],
            "item",
            {
                "item_a": [1, 3],
                "item_b": [2, 4],
                "item_c": [np.nan, 5],
            },
        ),
        # test sub-element type is list-like
        (
            None,
            "_",
            True,
            [(1, 2), (3, [4, 5]), [[6]]],
            "item",
            {
                "item_0": [1, 3, 6],
                "item_1": [2, 4, np.nan],
                "item_2": [np.nan, 5, np.nan],
            },
        ),
        (
            None,
            "_",
            False,
            [[1], [2]],
            "item",
            {"item": [1, 2]},
        ),
    ],
)
def test_work(suffix, delimiter, flatten, data, name, expected):
    s = pd.Series(data, name=name)
    expected = pd.DataFrame(expected)
    result = s.expand(suffix=suffix, delimiter=delimiter, flatten=flatten)

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "suffix, data, name, error",
    [
        # len(suffix) < max length of elements
        (
            ["a"],
            [(1, 2)],
            "item",
            ValueError,
        ),
        # name of series is None
        (
            None,
            [(1, 2)],
            None,
            ValueError,
        ),
    ],
)
def test_error(suffix, data, name, error):
    s = pd.Series(data, name=name)

    with pytest.raises(error):
        s.expand(suffix=suffix)


def test_not_list_like_type():
    result = pd.Series([1, 2, 3], name="item").expand()
    expected = pd.DataFrame({"item": [1, 2, 3]})

    assert_frame_equal(result, expected)
