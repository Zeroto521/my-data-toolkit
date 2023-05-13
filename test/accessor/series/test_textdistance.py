import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import textdistance


rapidfuzz = pytest.importorskip("rapidfuzz")


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


@pytest.mark.parametrize(
    "s, other, align, method, expected",
    [
        # normal case
        (
            pd.Series(["hello", "world"]),
            "python",
            True,
            None,
            pd.Series([36.36, 18.18]),
        ),
        # test method
        (
            pd.Series(["hi", "python"]),
            "",
            True,
            rapidfuzz.distance.Levenshtein.distance,
            pd.Series([2, 6]),
        ),
        # test None and nan
        # NOTE: requires rapidfuzz >= 3.x
        (
            pd.Series(["hi", "python", None, None, float("nan"), "?"]),
            pd.Series([None, float("nan"), None, float("nan"), float("nan"), "!"]),
            True,
            None,
            pd.Series([0] * 6),
        ),
        # test other is None
        # NOTE: requires rapidfuzz >= 3.x
        (
            pd.Series(["hi", "python", None, None, float("nan"), "?"]),
            None,
            True,
            None,
            pd.Series([0] * 6),
        ),
        # test other is nan
        # NOTE: requires rapidfuzz >= 3.x
        (
            pd.Series(["hi", "python", None, None, float("nan"), "?"]),
            float("nan"),
            True,
            None,
            pd.Series([0] * 6),
        ),
    ],
)
def test_work(s, other, align, method, expected):
    result = textdistance(s, other, align=align, method=method)

    assert_series_equal(
        result,
        expected,
        check_dtype=False,
        rtol=1e-3,
    )
