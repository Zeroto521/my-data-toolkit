import pandas as pd

from .._checking import check_dataframe_type
from ..accessor import ColumnAccessor  # noqa
from ..accessor import FilterInAccessor  # noqa
from .base import Transformer


class DataFrameTF(Transformer):
    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)


class AssignTF(Transformer):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.assign(*args, **kwargs)


class AppendTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.append(*args, **kwargs)


class DropTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.drop(*args, **kwargs)


class EvalTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.eval(*args, **kwargs)


class FillnaTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.fillna(*args, **kwargs)


class FilterInTF(DataFrameTF):
    def transform(self, X, *_):
        self.validate(X)

        return X.filterin(*self.args, **self.kwargs)


class FilterTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.filter(*args, **kwargs)


class GetTF(Transformer):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.get(*args, **kwargs)


class QueryTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.query(*args, **kwargs)


class ReplaceTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.replace(*args, **kwargs)


class SelectDtypesTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return pd.DataFrame.select_dtypes(*args, **kwargs)
