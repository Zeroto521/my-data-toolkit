import pandas as pd
import pytest
import numpy as np
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import equal


@pytest.mark.parametrize(
    "s, other, align, error",
    [
        (pd.Series([1, 2, 3]), [1, 2], True, ValueError),
        (pd.Series([1, 2, 3]), pd.Series([1, 2]), False, ValueError),
    ],
)
def test_error(s, other, align, error):
    with pytest.raises(error):
        equal(s, other, align=align)


@pytest.mark.parametrize(
    "s, other, align, warning",
    [
        (
            pd.Series([1, 2, 3]),
            pd.Series([1, 2, 3], index=[2, 1, 0]),
            True,
            UserWarning,
        ),
        (
            pd.Series([1, 2, 3]),
            pd.Series([1, 2], index=[1, 2]),
            True,
            UserWarning,
        ),
    ],
)
def test_warning(s, other, align, warning):
    with pytest.warns(warning):
        equal(s, other, align=align)


@pytest.mark.parametrize(
    "s, other, align, expected",
    [
        # test scalar
        (
            pd.Series([1, 2, 3]),
            2,
            True,
            pd.Series([False, True, False]),
        ),
        (
            pd.Series([1, 2, 3]),
            "2",
            True,
            pd.Series([False, False, False]),
        ),
        (
            pd.Series([1, 2, 3]),
            float,
            True,
            pd.Series([False, False, False]),
        ),
        # test list
        (
            pd.Series([1, 2, 3]),
            [2, 2, 2],
            True,
            pd.Series([False, True, False]),
        ),
        # test ndarray
        (
            pd.Series([1, 2, 3]),
            np.array([2, 2, 2]),
            True,
            pd.Series([False, True, False]),
        ),
        # test Series
        (
            pd.Series([1, 2, 3]),
            pd.Series([1, 2, 3], index=[2, 1, 0]),
            True,
            pd.Series([False, True, False]),
        ),
        (
            pd.Series([1, 2, 3]),
            pd.Series([1, 2, 3], index=[2, 1, 0]),
            True,
            pd.Series([False, True, False]),
        ),
        (
            pd.Series([1, 2, 3]),
            pd.Series([1, 2, 3], index=[1, 2, 3]),
            True,
            pd.Series([False, False, False, False]),
        ),
        (
            pd.Series([1, 2, 3]),
            pd.Series([2, 3, 1], index=[1, 2, 3]),
            True,
            pd.Series([False, True, True, False]),
        ),
    ],
)
def test_work(s, other, align, expected):
    result = s.equal(other, align=align)

    assert_series_equal(result, expected)
