from typing import Any, List

import pandas as pd
from sklearn.base import TransformerMixin

from ._typing import Pd


class DummifierTF(TransformerMixin):

    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def fit(self, *_):
        return self

    def transform(self, X: Pd):
        if self.cols:
            return pd.get_dummies(X[self.cols], columns=self.cols)
        else:
            return pd.get_dummies(X, columns=X.col.columns)

    def fit_transform(self, X: Pd, *_):
        return self.transform(X)


class SelectedTF(TransformerMixin):

    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def fit(self, *_):
        return self

    def transform(self, X: Pd):
        return X[self.cols] if self.cols else X

    def fit_transform(self, X: Pd, *_):
        return self.transform(X)

    def inverse_transform(self, X: Any, *_):
        return X
