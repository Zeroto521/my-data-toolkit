from __future__ import annotations

import pandas as pd

from ._typing import Pd


@pd.api.extensions.register_dataframe_accessor("col")
@pd.api.extensions.register_series_accessor("col")
class PandasColumnAccessor:
    def __init__(self, obj: Pd):
        self._obj = obj

    @property
    def columns(self) -> str | pd.core.indexes.base.Index:
        if isinstance(self._obj, pd.Series):
            return self._obj.name
        else:
            return self._obj.columns
