import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.dataframe import equal


@pytest.mark.parametrize(
    "df, other, align, axis, error",
    [
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [1, 2, 3],
            True,
            0,
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [1, 2],
            True,
            1,
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [[1]],
            True,
            0,
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [[1]],
            True,
            1,
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame([[1]]),
            False,
            0,
            ValueError,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2]),
            False,
            1,
            ValueError,
        ),
    ],
)
def test_error(df, other, align, axis, error):
    with pytest.raises(error):
        equal(df, other, align=align, axis=axis)


@pytest.mark.parametrize(
    "s, other, align, axis, warning",
    [
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2, 3]),
            True,
            0,
            UserWarning,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2, 3], index=[3, 2, 1]),
            True,
            1,
            UserWarning,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}, index=[1, 2, 3]),
            True,
            0,
            UserWarning,
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"a": [1, 2, 3]}),
            True,
            0,
            UserWarning,
        ),
    ],
)
def test_warning(s, other, align, axis, warning):
    with pytest.warns(warning):
        equal(s, other, align=align, axis=axis)


@pytest.mark.parametrize(
    "df, other, align, axis, expected",
    [
        # test scalar
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            2,
            True,
            0,
            pd.DataFrame({"a": [False, True, False], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            1,
            True,
            1,
            pd.DataFrame({"a": [True, False, False], "b": [False, False, True]}),
        ),
        # test 1d list
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [1, 2],
            True,
            0,
            pd.DataFrame({"a": [True, False, False], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [1, 2, 3],
            True,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        # test 1d ndarrray
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            np.array([1, 2]),
            True,
            0,
            pd.DataFrame({"a": [True, False, False], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            np.array([1, 2, 3]),
            True,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        # test 1d series
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2], index=["a", "b"]),
            True,
            0,
            pd.DataFrame({"a": [True, False, False], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2]),
            False,
            0,
            pd.DataFrame({"a": [True, False, False], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.Series([1, 2, 3]),
            True,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        # test 2d list
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            [[1, 1], [2, 2], [3, 3]],
            True,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        # test 2d dataframe
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"a": [1, 2, 3]}),
            True,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, False, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"a": [1, 2, 3]}),
            False,
            0,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"c": [1, 2, 3]}),
            False,
            1,
            pd.DataFrame({"a": [True, True, True], "b": [False, True, False]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}),
            pd.DataFrame({"c": [1, 2, 3]}),
            True,
            1,
            pd.DataFrame(
                {
                    "a": [False, False, False],
                    "b": [False, False, False],
                    "c": [False, False, False],
                },
            ),
        ),
    ],
)
def test_work(df, other, align, axis, expected):
    result = df.equal(other, align=align, axis=axis)

    assert_frame_equal(result, expected)
