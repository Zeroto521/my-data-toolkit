from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from numpy import ndarray, ravel
from pandas import DataFrame
from sklearn.base import TransformerMixin
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler

from ._checking import check_dataframe_type


class Transformer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.validate: Optional[Callable] = None
        self.operate: Optional[Callable] = None

    def fit(self, *_):
        return self

    def transform(self, X, *_):
        if self.validate:
            self.validate(X)

        if not self.operate:
            raise ValueError("operate is missing.")

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.validate = check_dataframe_type


class GetTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.get


class FillnaTF(DataFrameTF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.fillna


class EvalTF(DataFrameTF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.eval


class QueryTF(DataFrameTF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.query


class DropTF(DataFrameTF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.drop


class AppendTF(DataFrameTF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.append


#
# numpy's operation
#


class RavelTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = ravel
