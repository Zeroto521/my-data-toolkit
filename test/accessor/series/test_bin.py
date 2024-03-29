import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import bin  # noqa: F401


@pytest.mark.parametrize(
    "bins, labels, right, expected",
    [
        (
            [-np.inf, 1, 10, 20, 30, np.inf],
            ["a", "b", "c", "d", "e"],
            False,
            ["b", "c", "d", "e", "e", "e"],
        ),
        (
            [-np.inf, 1, 10, 20, 30, np.inf],
            ["a", "b", "c", "d", "e"],
            True,
            ["a", "b", "c", "d", "e", "e"],
        ),
        (
            [-np.inf, 1, 10, 20],
            ["a", "b", "c"],
            True,
            ["a", "b", "c"] + [np.nan] * 3,
        ),
        (
            [1, 10, 20],
            ["a", "b"],
            False,
            ["a", "b"] + [np.nan] * 4,
        ),
        (
            [-np.inf, np.inf],
            ["a"],
            False,
            ["a"] * 6,
        ),
    ],
)
def test_work(bins, labels, right, expected):
    s = pd.Series([1, 10, 20, 30, 40, 50])
    result = s.bin(
        bins=bins,
        labels=labels,
        right=right,
        ordered=False,
    )
    expected = pd.Series(
        expected,
        dtype=pd.CategoricalDtype(categories=labels),
    )

    assert_series_equal(result, expected)
