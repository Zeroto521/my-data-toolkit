import pandas as pd
import pytest

from dtoolkit.accessor.series import textdistance


@pytest.mark.parametrize(
    "s, other, align, error",
    [
        # s is not string dtype
        (
            pd.Series([1, 2]),
            "a",
            True,
            TypeError,
        ),
        # other is not string dtype
        (
            pd.Series(["hello", "world"]),
            1,
            True,
            TypeError,
        ),
        # other is not string dtype
        (
            pd.Series(["hello", "world"]),
            [1],
            True,
            TypeError,
        ),
        # other is not string dtype
        (
            pd.Series(["hello", "world"]),
            pd.Series([1]),
            True,
            TypeError,
        ),
        # other is not 1d array
        (
            pd.Series(["hello", "world"]),
            [["python"]],
            True,
            TypeError,
        ),
        # other is not 1d array
        (
            pd.Series(["hello", "world"]),
            pd.Series([["python"]]),
            True,
            TypeError,
        ),
        # other is not 1d array and not string dtype
        (
            pd.Series(["hello", "world"]),
            [[1]],
            True,
            TypeError,
        ),
        # other is not 1d array and not string dtype
        (
            pd.Series(["hello", "world"]),
            pd.Series([[1]]),
            True,
            TypeError,
        ),
        # test align
        (
            pd.Series(["hello", "world"]),
            pd.Series("python"),
            False,
            ValueError,
        ),
    ],
)
def test_error(s, other, align, error):
    with pytest.raises(error):
        textdistance(s, other, align=align)
