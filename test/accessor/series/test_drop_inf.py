import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.accessor.series import drop_inf  # noqa: F401
from test.accessor.data import s
from test.accessor.data import s_inf


@pytest.mark.parametrize(
    "inf, df, expected",
    [
        ("all", s, s),
        ("all", pd.concat((s, s_inf)), s.rename(None)),
        ("pos", s_inf, pd.Series([-np.inf], index=[1])),
        ("+", s_inf, pd.Series([-np.inf], index=[1])),
        ("neg", s_inf, pd.Series([np.inf])),
        ("-", s_inf, pd.Series([np.inf])),
    ],
)
def test_work(inf, df, expected):
    result = df.drop_inf(inf=inf)

    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "error, inf",
    [
        (ValueError, np.inf),
        (ValueError, None),
    ],
)
def test_error(error, inf):
    with pytest.raises(error):
        s_inf.drop_inf(inf=inf)
