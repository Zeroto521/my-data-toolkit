from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from numpy import ravel
from pandas import DataFrame
from sklearn.base import TransformerMixin

from ._checking import check_dataframe_type


class TransformerBase(TransformerMixin):
    def fit(self, *_):
        return self

    def fit_transform(self, X: DataFrame, *_) -> DataFrame:
        return self.transform(X)


def transformer_factory(
    func, check: Optional[Callable] = check_dataframe_type
) -> TransformerBase:
    class TF(TransformerBase):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def transform(self, X):
            if check:
                check_dataframe_type(X)

            return func(X, *self.args, **self.kwargs)

    return TF


#
# Pandas's operation
#


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


FillnaTF = transformer_factory(DataFrame.fillna)
EvalTF = transformer_factory(DataFrame.eval)
QueryTF = transformer_factory(DataFrame.query)


#
# numpy's operation
#

RavelTF = transformer_factory(ravel, check=None)
