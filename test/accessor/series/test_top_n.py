import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import top_n  # noqa: F401


@pytest.mark.parametrize(
    "n, largest, keep, expected",
    [
        (
            4,
            True,
            "first",
            {
                "France": 65000000,
                "Italy": 59000000,
                "Brunei": 434000,
                "Malta": 434000,
            },
        ),
        (
            4,
            True,
            "all",
            {
                "France": 65000000,
                "Italy": 59000000,
                "Brunei": 434000,
                "Malta": 434000,
                "Maldives": 434000,
            },
        ),
        (
            2,
            False,
            "last",
            {"Montserrat": 5200, "Anguilla": 11300},
        ),
        (
            2,
            False,
            "all",
            {
                "Montserrat": 5200,
                "Nauru": 11300,
                "Tuvalu": 11300,
                "Anguilla": 11300,
            },
        ),
    ],
)
def test_work(n, largest, keep, expected):
    s = pd.Series(
        {
            "Italy": 59000000,
            "France": 65000000,
            "Brunei": 434000,
            "Malta": 434000,
            "Maldives": 434000,
            "Iceland": 337000,
            "Nauru": 11300,
            "Tuvalu": 11300,
            "Anguilla": 11300,
            "Montserrat": 5200,
        },
    )
    result = s.top_n(n=n, largest=largest, keep=keep)
    expected = pd.Series(expected)

    assert_series_equal(result, expected)
