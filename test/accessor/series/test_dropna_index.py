import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import dropna_index


def test_error():
    with pytest.raises(ValueError):
        s = pd.Series([1, 2, 3, 4, 5])
        s.dropna_index(how="whatever")


@pytest.mark.parametrize(
    "s, how, expected",
    [
        (
            pd.Series([1, 2, 3], index=[[1, 2, None], ["red", None, None]]),
            "any",
            pd.Series([1], index=[[1], ["red"]]),
        ),
        (
            pd.Series([1, 2, 3], index=[[1, 2, None], ["red", None, None]]),
            "all",
            pd.Series([1, 2], index=[[1, 2], ["red", None]]),
        ),
    ],
)
def test_MultiIndex(s, how, expected):
    result = dropna_index(s, how=how)

    assert_series_equal(result, expected)
