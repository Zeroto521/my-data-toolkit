from test.accessor.conftest import s
from test.accessor.conftest import s_inf

import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor.series import drop_inf  # noqa


@pytest.mark.parametrize(
    "inf, df, expt",
    [
        ("all", s, s),
        ("all", pd.concat((s, s_inf)), s),
        ("pos", s_inf, pd.Series([-np.inf], index=[1])),
        ("+", s_inf, pd.Series([-np.inf], index=[1])),
        ("neg", s_inf, pd.Series([np.inf])),
        ("-", s_inf, pd.Series([np.inf])),
    ],
)
def test_work(inf, df, expt):
    res = df.drop_inf(inf=inf)

    assert res.equals(expt)


def test_inplace_is_true():
    self_s = pd.concat((s, s_inf))
    res = self_s.drop_inf(inplace=True)

    assert res is None
    assert self_s.equals(s)


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
