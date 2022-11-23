import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.series import textdistance_matrix


pytest.importorskip("thefuzz")


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
                [[100, 36], [20, 18]],
                index=["s11", "s12"],
                columns=["s21", "s22"],
            ),
        ),
        # method is not None
        (
            pd.Series(["hello", "world!"]),
            pd.Series(["hi", "pythonista"]),
            lambda *xy: sum(map(len, xy)),
            pd.DataFrame([[7, 15], [8, 16]]),
        ),
    ],
)
def test_work(s, other, method, expected):
    result = s.textdistance_matrix(other, method=method)

    assert_frame_equal(result, expected)


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
