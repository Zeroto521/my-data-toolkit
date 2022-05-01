import pandas as pd
import pytest

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.register import register_index_method
from dtoolkit.accessor.register import register_series_method


def base_name_or_columns(pd_obj):
    if isinstance(pd_obj, (pd.Series, pd.Index)):
        return pd_obj.name

    return pd_obj.columns.tolist()


@register_index_method
@register_series_method
@register_dataframe_method
def name_or_columns(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_name_or_columns(pd_obj)


@register_index_method()
@register_series_method()
@register_dataframe_method()
def name_or_columns_1(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_name_or_columns(pd_obj)


@register_index_method(name="alias_name_or_columns")
@register_series_method(name="alias_name_or_columns")
@register_dataframe_method(name="alias_name_or_columns")
def name_or_columns_2(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_name_or_columns(pd_obj)


@register_index_method("alias_name_or_columns_1")
@register_series_method("alias_name_or_columns_1")
@register_dataframe_method("alias_name_or_columns_1")
def name_or_columns_3(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_name_or_columns(pd_obj)


df = pd.DataFrame(
    {
        "a": [1, 2],
        "b": [3, 4],
    },
    index=pd.Index(
        ["x", "y"],
        name="z",
    ),
)


@pytest.mark.parametrize(
    "data, name",
    [
        (df, "name_or_columns"),
        (df, "name_or_columns_1"),
        (df, "alias_name_or_columns"),
        (df, "alias_name_or_columns_1"),
        (df.a, "name_or_columns"),
        (df.b, "name_or_columns_1"),
        (df.a, "alias_name_or_columns"),
        (df.b, "alias_name_or_columns_1"),
        (df.index, "name_or_columns"),
        (df.a.index, "name_or_columns_1"),
        (df.b.index, "alias_name_or_columns"),
        (df.index, "alias_name_or_columns_1"),
    ],
)
def test_method_hooked_exist(data, name):
    assert hasattr(data, name)


@pytest.mark.parametrize(
    "data, name, excepted",
    [
        (df, "name_or_columns", ["a", "b"]),
        (df.a, "name_or_columns", "a"),
        (df.a.index, "name_or_columns", "z"),
        (df, "name_or_columns_1", ["a", "b"]),
        (df.b, "name_or_columns_1", "b"),
        (df.b.index, "name_or_columns_1", "z"),
        (df, "alias_name_or_columns", ["a", "b"]),
        (df.b, "alias_name_or_columns", "b"),
        (df.index, "alias_name_or_columns", "z"),
        (df, "alias_name_or_columns_1", ["a", "b"]),
        (df.a, "alias_name_or_columns_1", "a"),
        (df.index, "alias_name_or_columns_1", "z"),
    ],
)
def test_work(data, name, excepted):
    result = getattr(data, name)()

    assert result == excepted


@pytest.mark.parametrize(
    "data, name, attr, excepted",
    [
        (df, "name_or_columns", "__name__", name_or_columns.__name__),
        (df.a, "name_or_columns", "__name__", name_or_columns.__name__),
        (df.index, "name_or_columns", "__name__", name_or_columns.__name__),
        (df, "name_or_columns", "__doc__", name_or_columns.__doc__),
        (df.a, "name_or_columns", "__doc__", name_or_columns.__doc__),
        (df.a.index, "name_or_columns", "__doc__", name_or_columns.__doc__),
        (df, "name_or_columns_1", "__name__", name_or_columns_1.__name__),
        (df.b, "name_or_columns_1", "__name__", name_or_columns_1.__name__),
        (df.b.index, "name_or_columns_1", "__name__", name_or_columns_1.__name__),
        (df, "name_or_columns_1", "__doc__", name_or_columns_1.__doc__),
        (df.a, "name_or_columns_1", "__doc__", name_or_columns_1.__doc__),
        (df.index, "name_or_columns_1", "__doc__", name_or_columns_1.__doc__),
        (df, "alias_name_or_columns", "__doc__", name_or_columns_2.__doc__),
        (df.b, "alias_name_or_columns", "__doc__", name_or_columns_2.__doc__),
        (df.b.index, "alias_name_or_columns", "__doc__", name_or_columns_2.__doc__),
        (df, "alias_name_or_columns_1", "__doc__", name_or_columns_2.__doc__),
        (df.a, "alias_name_or_columns_1", "__doc__", name_or_columns_2.__doc__),
        (df.index, "alias_name_or_columns_1", "__doc__", name_or_columns_2.__doc__),
    ],
)
def test_method_hooked_attr(data, name, attr, excepted):
    method = getattr(data, name)
    result = getattr(method, attr)

    assert result == excepted
