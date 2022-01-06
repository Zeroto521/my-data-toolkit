import pandas as pd
import pytest

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.register import register_series_method


@register_dataframe_method
@register_series_method
def names(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """
    if isinstance(pd_obj, pd.Series):
        return pd_obj.name

    return pd_obj.columns.tolist()


@register_dataframe_method()
@register_series_method()
def names_1(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """
    if isinstance(pd_obj, pd.Series):
        return pd_obj.name

    return pd_obj.columns.tolist()


@register_dataframe_method(name="name_or_columns")
@register_series_method(name="name_or_columns")
def names_2(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """
    if isinstance(pd_obj, pd.Series):
        return pd_obj.name

    return pd_obj.columns.tolist()


df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})


@pytest.mark.parametrize(
    "data, name",
    [
        (df, "names"),
        (df.a, "names"),
        (df, "names_1"),
        (df.a, "names_1"),
        # (df, "name_or_columns"),
        # (df.a, "name_or_columns"),
    ],
)
def test_method_hooked_exist(data, name):
    assert hasattr(data, name)


@pytest.mark.parametrize(
    "data, name, excepted",
    [
        (df, "names", ["a", "b"]),
        (df.a, "names", "a"),
        (df, "names_1", ["a", "b"]),
        (df.a, "names_1", "a"),
        (df, "name_or_columns", ["a", "b"]),
        (df.a, "name_or_columns", "a"),
    ],
)
def test_work(data, name, excepted):
    result = getattr(data, name)()

    assert result == excepted


@pytest.mark.parametrize(
    "data, name, attr, excepted",
    [
        (df, "names", "__name__", names.__name__),
        (df.a, "names", "__name__", names.__name__),
        (df, "names", "__doc__", names.__doc__),
        (df.a, "names", "__doc__", names.__doc__),
        (df, "names_1", "__name__", names_1.__name__),
        (df.a, "names_1", "__name__", names_1.__name__),
        (df, "names_1", "__doc__", names_1.__doc__),
        (df.a, "names_1", "__doc__", names_1.__doc__),
        (df, "name_or_columns", "__doc__", names_2.__doc__),
        (df.a, "name_or_columns", "__doc__", names_2.__doc__),
    ],
)
def test_method_hooked_attr(data, name, attr, excepted):
    method = getattr(data, name)
    result = getattr(method, attr)

    assert result == excepted
