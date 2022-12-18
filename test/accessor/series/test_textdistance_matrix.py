import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.series import textdistance_matrix


rapidfuzz = pytest.importorskip("rapidfuzz")


@pytest.mark.parametrize(
    "s, other, method, expected",
    [
        # other is None
        (
            pd.Series(["hello", "world"]),
            None,
            None,
            pd.DataFrame([[100, 20], [20, 100]]),
        ),
        # other is not None
        (
            pd.Series(["hello", "world"], index=["s11", "s12"]),
            pd.Series(["hello", "python"], index=["s21", "s22"]),
            None,
            pd.DataFrame(
                [[100, 36.36], [20, 18.18]],
                index=["s11", "s12"],
                columns=["s21", "s22"],
            ),
        ),
        # method is not None
        (
            pd.Series(["hello", "world!"]),
            pd.Series(["hi", "pythonista"]),
            rapidfuzz.string_metric.levenshtein,
            pd.DataFrame([[4, 9], [6, 9]]),
        ),
        # other elements contain None or nan
        (
            pd.Series(["hello", "world", "!"]),
            pd.Series(["hi!", None, float("nan")]),
            None,
            pd.DataFrame([[25, 0, 0], [0, 0, 0], [50, 0, 0]]),
        ),
    ],
)
def test_work(s, other, method, expected):
    result = s.textdistance_matrix(other, method=method)

    assert_frame_equal(
        result,
        expected,
        check_dtype=False,
        rtol=1e-3,
    )


@pytest.mark.parametrize(
    "s, other, error",
    [
        # other is not Series
        (
            pd.Series(["hello", "world!"]),
            "hi",
            TypeError,
        ),
        # other is not Series
        (
            pd.Series(["hello", "world!"]),
            ["hi"],
            TypeError,
        ),
        # other is not Series(string)
        (
            pd.Series(["hello", "world!"]),
            pd.Series(1),
            TypeError,
        ),
    ],
)
def test_error(s, other, error):
    with pytest.raises(error):
        textdistance_matrix(s, other)
