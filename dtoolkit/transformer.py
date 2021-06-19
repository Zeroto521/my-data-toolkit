from __future__ import annotations

from typing import List

import pandas as pd
from sklearn.base import TransformerMixin

from ._typing import Pd
from ._checking import bad_condition_raise_error


class TransformerBase(TransformerMixin):
    def fit(self):
        return self


class SelectorTF(TransformerBase):
    def __init__(self, cols: List[str] = None):
        self.cols = cols

    def transform(self, X: pd.DataFrame) -> Pd:
        bad_condition_raise_error(
            not isinstance(X, pd.DataFrame),
            TypeError,
            "The input is not a 'DataFrame' type.",
        )

        return X[self.cols] if self.cols else X

    def fit_transform(self, X: pd.DataFrame, *_) -> Pd:
        return self.transform(X)

    def inverse_transform(self, X: pd.DataFrame, *_) -> Pd:
        return X
