import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.dataframe import repeat  # noqa: F401


@pytest.mark.parametrize(
    "repeat, axis, expected",
    [
        (1, 0, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
        (1, 1, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
        (
            2,
            0,
            pd.DataFrame(
                {
                    "a": [1, 1, 2, 2],
                    "b": [3, 3, 4, 4],
                },
                index=[0, 0, 1, 1],
            ),
        ),
        (
            2,
            1,
            pd.DataFrame(
                [
                    [1, 1, 3, 3],
                    [2, 2, 4, 4],
                ],
                columns=["a", "a", "b", "b"],
            ),
        ),
        (
            [1, 2],
            1,
            pd.DataFrame(
                [
                    [1, 3, 3],
                    [2, 4, 4],
                ],
                columns=["a", "b", "b"],
            ),
        ),
    ],
)
def test_work(repeat, axis, expected):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = df.repeat(repeat, axis=axis)

    assert_frame_equal(result, expected)


@pytest.mark.parametrize("axis", [-1, 3, None])
def test_error(axis):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(ValueError):
        df.repeat(2, axis)
