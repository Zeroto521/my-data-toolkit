from __future__ import annotations

import numpy as np
import pandas as pd
from more_itertools import flatten
from scipy import sparse
from sklearn.base import TransformerMixin
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.preprocessing import MinMaxScaler as SKMinMaxScaler
from sklearn.preprocessing import OneHotEncoder as SKOneHotEncoder

from ._checking import check_dataframe_type
from ._checking import istype
from ._typing import PandasTypeList
from .accessor import FilterInAccessor  # noqa


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


class FeatureUnion(SKFeatureUnion):
    def _hstack(self, Xs):
        if any(sparse.issparse(f) for f in Xs):
            return sparse.hstack(Xs).tocsr()

        if all(istype(i, PandasTypeList) for i in Xs):
            return pd.concat(Xs, axis=1)

        return np.hstack(Xs)


def _change_data_to_df(
    data: np.ndarray,
    df: pd.DataFrame | np.ndarray,
) -> pd.DataFrame | np.ndarray:
    if isinstance(df, pd.DataFrame):
        return pd.DataFrame(data, columns=df.columns, index=df.index)

    return data


class MinMaxScaler(SKMinMaxScaler):
    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        return _change_data_to_df(X_new, X)

    def inverse_transform(self, X, *_):
        X_new = super().inverse_transform(X, *_)

        return _change_data_to_df(X_new, X)


class OneHotEncoder(SKOneHotEncoder):
    def __init__(
        self,
        categories="auto",
        drop=None,
        sparse=False,
        dtype=np.float64,
        handle_unknown="error",
    ):
        super().__init__(
            categories=categories,
            drop=drop,
            sparse=sparse,
            dtype=dtype,
            handle_unknown=handle_unknown,
        )

    def transform(self, X, *_):
        X_new = super().transform(X, *_)

        if self.sparse is False:
            categories = flatten(self.categories_)
            return pd.DataFrame(X_new, columns=categories)

        return X_new


#
# Pandas's operation
#


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


#
# numpy's operation
#


class RavelTF(Transformer):
    def operate(self, *args, **kwargs):
        return np.ravel(*args, **kwargs)
