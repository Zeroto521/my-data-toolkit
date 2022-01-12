import pandas as pd
import pytest

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.register import register_series_method


def base_names(pd_obj):
    if isinstance(pd_obj, pd.Series):
        return pd_obj.name

    return pd_obj.columns.tolist()


@register_dataframe_method
@register_series_method
def method_names(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_names(pd_obj)


@register_dataframe_method()
@register_series_method()
def method_names_1(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_names(pd_obj)


@register_dataframe_method(name="method_name_or_columns")
@register_series_method(name="method_name_or_columns")
def method_names_2(pd_obj):
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_names(pd_obj)


@register_dataframe_method("method_name_or_columns_1")
@register_series_method("method_name_or_columns_1")
def method_names_3(pd_obj):

    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    """

    return base_names(pd_obj)


class base_class:
    def __init__(self, pd_obj):
        self.pd_obj = pd_obj


@register_dataframe_method
@register_series_method
class class_names(base_class):
    def attr_property(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)

    def attr_method(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)


@register_dataframe_method()
@register_series_method()
class class_names_1(base_class):
    def attr_property(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)

    def attr_method(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)


@register_dataframe_method(name="class_name_or_columns")
@register_series_method(name="class_name_or_columns")
class class_names_2(base_class):
    def attr_property(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)

    def attr_method(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)


@register_dataframe_method("class_name_or_columns_1")
@register_series_method("class_name_or_columns_1")
class class_names_3(base_class):
    def attr_property(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)

    def attr_method(self):
        """
        An API to gather :attr:`~pandas.Series.name` and
        :attr:`~pandas.DataFrame.columns` to one.
        """

        return base_names(self.pd_obj)


df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})


class TestMethod:
    @pytest.mark.parametrize(
        "data, name",
        [
            (df, "method_names"),
            (df.a, "method_names"),
            (df, "method_names_1"),
            (df.a, "method_names_1"),
            (df, "method_name_or_columns"),
            (df.a, "method_name_or_columns"),
            (df, "method_name_or_columns_1"),
            (df.a, "method_name_or_columns_1"),
        ],
    )
    def test_method_hooked_exist(self, data, name):
        assert hasattr(data, name)

    @pytest.mark.parametrize(
        "data, name, excepted",
        [
            (df, "method_names", ["a", "b"]),
            (df.a, "method_names", "a"),
            (df, "method_names_1", ["a", "b"]),
            (df.a, "method_names_1", "a"),
            (df, "method_name_or_columns", ["a", "b"]),
            (df.a, "method_name_or_columns", "a"),
            (df, "method_name_or_columns_1", ["a", "b"]),
            (df.a, "method_name_or_columns_1", "a"),
        ],
    )
    def test_work(self, data, name, excepted):
        result = getattr(data, name)()

        assert result == excepted

    @pytest.mark.parametrize(
        "data, name, attr, excepted",
        [
            (df, "method_names", "__name__", method_names.__name__),
            (df.a, "method_names", "__name__", method_names.__name__),
            (df, "method_names", "__doc__", method_names.__doc__),
            (df.a, "method_names", "__doc__", method_names.__doc__),
            (df, "method_names_1", "__name__", method_names_1.__name__),
            (df.a, "method_names_1", "__name__", method_names_1.__name__),
            (df, "method_names_1", "__doc__", method_names_1.__doc__),
            (df.a, "method_names_1", "__doc__", method_names_1.__doc__),
            (df, "method_name_or_columns", "__name__", method_names_2.__name__),
            (df.a, "method_name_or_columns", "__name__", method_names_2.__name__),
            (df, "method_name_or_columns", "__doc__", method_names_2.__doc__),
            (df.a, "method_name_or_columns", "__doc__", method_names_2.__doc__),
            (df, "method_name_or_columns_1", "__name__", method_names_3.__name__),
            (df.a, "method_name_or_columns_1", "__name__", method_names_3.__name__),
            (df, "method_name_or_columns_1", "__doc__", method_names_3.__doc__),
            (df.a, "method_name_or_columns_1", "__doc__", method_names_3.__doc__),
        ],
    )
    def test_method_hooked_attr(self, data, name, attr, excepted):
        method = getattr(data, name)
        result = getattr(method, attr)

        assert result == excepted


class TestClass:
    @pytest.mark.parametrize(
        "data, name",
        [
            (df, "class_names"),
            (df.a, "class_names"),
            (df, "class_names_1"),
            (df.a, "class_names_1"),
            (df, "class_name_or_columns"),
            (df.a, "class_name_or_columns"),
            (df, "class_name_or_columns_1"),
            (df.a, "class_name_or_columns_1"),
        ],
    )
    def test_class_hooked_exist(self, data, name):
        assert hasattr(data, name)

    @pytest.mark.parametrize(
        "data, name, attr, excepted",
        [
            (df, "class_names", "attr_property", ["a", "b"]),
            (df.a, "class_names", "attr_property", "a"),
            (df, "class_names_1", "attr_property", ["a", "b"]),
            (df.a, "class_names_1", "attr_property", "a"),
            (df, "class_name_or_columns", "attr_property", ["a", "b"]),
            (df.a, "class_name_or_columns", "attr_property", "a"),
            (df, "class_name_or_columns_1", "attr_property", ["a", "b"]),
            (df.a, "class_name_or_columns_1", "attr_property", "a"),
            (df, "class_names", "attr_method", ["a", "b"]),
            (df.a, "class_names", "attr_method", "a"),
            (df, "class_names_1", "attr_method", ["a", "b"]),
            (df.a, "class_names_1", "attr_method", "a"),
            (df, "class_name_or_columns", "attr_method", ["a", "b"]),
            (df.a, "class_name_or_columns", "attr_method", "a"),
            (df, "class_name_or_columns_1", "attr_method", ["a", "b"]),
            (df.a, "class_name_or_columns_1", "attr_method", "a"),
        ],
    )
    def test_work(self, data, name, attr, excepted):
        method = getattr(data, name)
        result = getattr(method, attr)
        if callable(result):
            result = result()

        assert result == excepted
