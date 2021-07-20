from __future__ import annotations

from typing import Callable, Optional

from numpy import ndarray, ravel
from pandas import DataFrame
from sklearn.base import TransformerMixin
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler

from ._checking import check_dataframe_type


class Transformer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def operate(self, X, *_, **__):
        return X

    def validate(self, *_, **__):
        ...

    def fit(self, *_):
        return self

    def transform(self, X, *_):
        self.validate(X)

        return self.operate(X, *self.args, **self.kwargs)

    def fit_transform(self, X, *_):
        return self.fit().transform(X)

    def inverse_transform(self, X, *_):
        return X


#
# Sklearn's operation
#


def _change_data_to_df(
    data: ndarray,
    df: DataFrame | ndarray,
) -> DataFrame | ndarray:
    if isinstance(df, DataFrame):
        return DataFrame(data, columns=df.columns, index=df.index)

    return data


class MinMaxScaler(SKMinMaxScaler):
    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        return _change_data_to_df(X_new, X)

    def inverse_transform(self, X, *_):
        X_new = super().inverse_transform(X, *_)

        return _change_data_to_df(X_new, X)


#
# Pandas's operation
#


class DataFrameTF(Transformer):
    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)


class GetTF(Transformer):
    def operate(self, *args, **kwargs):
        return DataFrame.get(*args, **kwargs)


class FillnaTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.fillna(*args, **kwargs)


class EvalTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.eval(*args, **kwargs)


class QueryTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.query(*args, **kwargs)


class DropTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.drop(*args, **kwargs)


class AppendTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.append(*args, **kwargs)


#
# numpy's operation
#


class RavelTF(Transformer):
    def operate(self, *args, **kwargs):
        return ravel(*args, **kwargs)
