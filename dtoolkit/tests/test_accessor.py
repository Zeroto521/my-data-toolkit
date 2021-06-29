import pandas as pd
import pytest
from dtoolkit.accessor import ColumnAccessor  # noqa

s = pd.Series(range(10), name="item")
d = pd.DataFrame({"a": range(10), "b": range(10)})


@pytest.mark.parametrize("df", [s, d])
def test_columnaccessor(df):
    if isinstance(df, pd.Series):
        assert df.cols() == df.name
    else:
        assert (df.cols() == df.columns).all()
