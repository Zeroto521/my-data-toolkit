import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.register import register_series_method


@register_dataframe_method
@register_series_method
def names(pd_obj):
    """
    A API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """
    if isinstance(pd_obj, pd.Series):
        return pd_obj.name

    return pd_obj.columns.tolist()


df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})


def test_method_hooked():
    assert hasattr(df, "names")
    assert hasattr(df.a, "names")


def test_work():
    assert df.names == ["a", "b"]
    assert df.a == "a"
