import numpy as np
import pandas as pd
import pytest
from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.accessor import DropInfAccessor  # noqa

s = pd.Series(range(10), name="item")
d = pd.DataFrame({"a": range(10), "b": range(10)})
s_inf = pd.Series([np.inf, -np.inf])


@pytest.mark.parametrize("df", [s, d])
def test_columnaccessor(df):
    if isinstance(df, pd.Series):
        assert df.cols() == df.name
    else:
        assert (df.cols() == df.columns).all()


@pytest.mark.parametrize("df", [s, s.append(s_inf)])
def test_dropinfaccessor(df):
    assert (df.dropinf() == s).all()
