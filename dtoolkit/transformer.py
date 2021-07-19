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


def _df_select_cols(
    df: DataFrame,
    cols: str | List[str] | Tuple[str],
) -> DataFrame:
    if not isinstance(cols, (str, list, tuple)):
        raise TypeError("cols must be 'str', 'list', or 'tuple'.")

    if isinstance(cols, str):
        cols = [cols]
    elif isinstance(cols, tuple):
        cols = list(cols)

    return df[cols] if cols else df


class SelectorTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = _df_select_cols
        self.validate = check_dataframe_type


class FillnaTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.fillna
        self.validate = check_dataframe_type


class EvalTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.eval
        self.validate = check_dataframe_type


class QueryTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.query
        self.validate = check_dataframe_type


class DropTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.drop
        self.validate = check_dataframe_type


class AppendTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = DataFrame.append
        self.validate = check_dataframe_type


#
# numpy's operation
#


class RavelTF(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operate = ravel
