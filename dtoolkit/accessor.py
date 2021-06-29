from __future__ import annotations

from typing import Callable

import pandas as pd

from ._typing import Pd


@pd.api.extensions.register_dataframe_accessor("cols")
@pd.api.extensions.register_series_accessor("cols")
class ColumnAccessor:
    def __new__(cls, pd_obj: Pd) -> Callable:
        def cols() -> str | pd.core.indexes.base.Index:
            if isinstance(pd_obj, pd.Series):
                return pd_obj.name
            else:
                return pd_obj.columns

        return cols
