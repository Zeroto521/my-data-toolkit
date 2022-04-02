import numpy as np
import pandas as pd
import pytest

import dtoolkit.accessor.series  # noqa


@pytest.mark.parametrize(
    "bins, labels, right, excepted",
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
def test_work(bins, labels, right, excepted):
    s = pd.Series([1, 10, 20, 30, 40, 50])
    res = s.bin(
        bins=bins,
        labels=labels,
        right=right,
    )
    excepted = pd.Series(
        excepted,
        dtype=pd.CategoricalDtype(categories=labels),
    )

    assert res.equals(excepted)


def test_inplace_is_true():
    s = pd.Series([1, 10, 20, 30, 40, 50])
    res = s.bin([10, 20], ["a"], inplace=True)
    excepted = pd.Series(
        [np.nan, np.nan, "a", np.nan, np.nan, np.nan],
        dtype="category",
    )

    assert res is None
    assert s.equals(excepted)
