from __future__ import annotations

import pandas as pd
from sklearn.base import TransformerMixin

from ._typing import Pd, bad_condition_raise_error


class TransformerBase(TransformerMixin):
    def fit(self):
        return self


class SelectorTF(TransformerBase):
    def __init__(self, cols: list[str] = None):
        self.cols = cols

    def transform(self, X: pd.DataFrame) -> Pd:
        bad_condition_raise_error(
            isinstance(X, pd.DataFrame),
            TypeError,
            "The input is not a 'DataFrame' type.",
        )

        return X[self.cols] if self.cols else X

    def fit_transform(self, X: pd.DataFrame, *_) -> Pd:
        return self.transform(X)

    def inverse_transform(self, X: pd.DataFrame, *_) -> Pd:
        return X
