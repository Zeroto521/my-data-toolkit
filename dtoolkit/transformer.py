from __future__ import annotations

from typing import List

import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import TransformerMixin

from ._typing import L, Pd
from .accessor import PandasColumnAccessor  # noqa


class TransformerBase(TransformerMixin):
    def fit(self):
        return self


class DummifierTF(TransformerBase):
    def __init__(self, cols: List[str] = None):
        self.cols = cols

    @doc(pd.get_dummies)
    def transform(self, X: Pd, **params) -> pd.DataFrame:
        columns = self.cols or X.cols()

        if self.cols:
            X = X[self.cols]

        return pd.get_dummies(X, columns=columns, **params)

    def fit_transform(self, X: Pd, *_) -> pd.DataFrame:
        return self.transform(X)


class SelectorTF(TransformerBase):
    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def transform(self, X: Pd) -> Pd:
        return X[self.cols] if self.cols else X

    def fit_transform(self, X: Pd, *_) -> Pd:
        return self.transform(X)

    def inverse_transform(self, X: L, *_) -> L:
        return X
