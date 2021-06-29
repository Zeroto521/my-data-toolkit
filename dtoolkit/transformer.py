from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import FunctionTransformer

from ._checking import bad_condition_raise_error


class TransformerBase(TransformerMixin):
    def fit(self):
        return self


class SelectorTF(TransformerBase):
    def __init__(self, cols: str | List[str] | Tuple[str] = None):
        if isinstance(cols, str):
            cols = [cols]

        self.cols = cols

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        bad_condition_raise_error(
            not isinstance(X, pd.DataFrame),
            TypeError,
            "The input is not a 'DataFrame' type.",
        )

        return X[self.cols] if self.cols else X

    def fit_transform(self, X: pd.DataFrame, *_) -> pd.DataFrame:
        return self.transform(X)

    def inverse_transform(self, X: pd.DataFrame, *_) -> pd.DataFrame:
        return X


RavelTF = FunctionTransformer(np.ravel)
