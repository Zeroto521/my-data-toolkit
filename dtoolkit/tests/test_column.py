import pandas as pd
from dtoolkit.accessor import PandasColumnAccessor  # noqa


def test_series_column():
    column = "item"
    s = pd.Series(range(10), name=column)
    assert s.col.columns == column


def test_dataframe_column():
    data = {"a": range(10), "b": range(10)}
    d = pd.DataFrame(data)
    assert list(d.col.columns) == list(data.keys())
