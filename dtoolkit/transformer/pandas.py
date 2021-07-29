from pandas import DataFrame
from pandas.util._decorators import doc

from .._checking import check_dataframe_type
from ..accessor import FilterInAccessor  # noqa
from .base import Transformer


class DataFrameTF(Transformer):
    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)


@doc(DataFrame.assign)
class AssignTF(Transformer):
    def operate(self, *args, **kwargs):
        return DataFrame.assign(*args, **kwargs)


@doc(DataFrame.append)
class AppendTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.append(*args, **kwargs)


@doc(DataFrame.drop)
class DropTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.drop(*args, **kwargs)


@doc(DataFrame.eval)
class EvalTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.eval(*args, **kwargs)


@doc(DataFrame.fillna)
class FillnaTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.fillna(*args, **kwargs)


class FilterInTF(DataFrameTF):
    def transform(self, X, *_):
        self.validate(X)

        return X.filterin(*self.args, **self.kwargs)


@doc(DataFrame.filter)
class FilterTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.filter(*args, **kwargs)


@doc(DataFrame.get)
class GetTF(Transformer):
    def operate(self, *args, **kwargs):
        return DataFrame.get(*args, **kwargs)


@doc(DataFrame.query)
class QueryTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.query(*args, **kwargs)


@doc(DataFrame.replace)
class ReplaceTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.replace(*args, **kwargs)


@doc(DataFrame.select_dtypes)
class SelectDtypesTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.select_dtypes(*args, **kwargs)
