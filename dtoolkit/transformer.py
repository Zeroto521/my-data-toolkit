from __future__ import annotations

from typing import List

import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import TransformerMixin

from ._typing import L, Pd
from .accessor import PandasColumnAccessor  # noqa


class DummifierTF(TransformerMixin):
    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def fit(self, *_):
        return self

    @doc(pd.get_dummies)
    def transform(self, X: Pd, **params):
        if self.cols:
            return pd.get_dummies(X[self.cols], columns=self.cols, **params)
        else:
            return pd.get_dummies(X, columns=X.col.columns, **params)

    def fit_transform(self, X: Pd, *_) -> pd.DataFrame:
        return self.transform(X)


class SelectorTF(TransformerMixin):
    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def fit(self, *_):
        return self

    def transform(self, X: Pd) -> Pd:
        return X[self.cols] if self.cols else X

    def fit_transform(self, X: Pd, *_) -> Pd:
        return self.transform(X)

    def inverse_transform(self, X: L, *_) -> L:
        return X
