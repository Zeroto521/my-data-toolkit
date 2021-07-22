from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

from ._typing import Pd


@pd.api.extensions.register_dataframe_accessor("cols")
@pd.api.extensions.register_series_accessor("cols")
def ColumnAccessor(pd_obj: Pd) -> Callable[..., Pd]:
    def cols() -> str | pd.core.indexes.base.Index:
        if isinstance(pd_obj, pd.Series):
            return pd_obj.name

        return pd_obj.columns

    return cols


@pd.api.extensions.register_series_accessor("dropinf")
def DropInfAccessor(s: pd.Series) -> Callable[..., pd.Series]:
    def dropinf() -> pd.Series:
        return s[~np.isinf(s)]

    return dropinf


@pd.api.extensions.register_dataframe_accessor("filterin")
def FilterInAccessor(
    df: pd.DataFrame,
) -> Callable[[dict[str, list[str]], bool], pd.DataFrame | None]:
    def filterin(
        cond: dict[str, list[str]],
        inplace: bool = False,
    ) -> pd.DataFrame | None:
        mask_all = df.isin(cond)
        mask_selected = mask_all[cond.keys()]
        result = df[mask_selected.all(axis=1)]

        if inplace:
            df._update_inplace(result)
            return None

        return result

    return filterin
