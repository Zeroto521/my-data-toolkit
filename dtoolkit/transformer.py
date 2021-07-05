from __future__ import annotations

from typing import List, Tuple

from numpy import ndarray, ravel
from pandas import DataFrame
from sklearn.base import TransformerMixin

from ._checking import check_dataframe_type
from ._typing import Pd


class TransformerBase(TransformerMixin):
    def fit(self, *_):
        return self

    def fit_transform(self, X: DataFrame, *_) -> DataFrame:
        return self.transform(X)


class SelectorTF(TransformerBase):
    def __init__(self, cols: str | List[str] | Tuple[str] = None):
        if isinstance(cols, str):
            cols = [cols]

        self.cols = cols

    def transform(self, X: DataFrame) -> DataFrame:
        check_dataframe_type(X)

        return X[self.cols] if self.cols else X

    def inverse_transform(self, X: DataFrame, *_) -> DataFrame:
        return X


class QueryTF(TransformerBase):
    def __init__(self, expr: str):
        self.expr = expr

    def transform(self, X: DataFrame) -> DataFrame:
        check_dataframe_type(X)

        return X.query(self.expr)


class EvalTF(TransformerBase):
    def __init__(self, expr: str):
        self.expr = expr

    def transform(self, X: DataFrame) -> DataFrame:
        check_dataframe_type(X)

        return X.eval(self.expr)


class RavelTF(TransformerBase):
    def transform(self, X: Pd | ndarray | List) -> ndarray:
        return ravel(X)

    def fit_transform(self, X: Pd | ndarray | List, *_) -> ndarray:
        return self.transform(X)
