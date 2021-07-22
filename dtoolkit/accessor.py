from __future__ import annotations

from typing import Callable

import pandas as pd
from numpy import inf

from ._typing import Pd


@pd.api.extensions.register_dataframe_accessor("cols")
@pd.api.extensions.register_series_accessor("cols")
def ColumnAccessor(pd_obj: Pd) -> Callable[..., Pd]:
    def cols() -> str | pd.core.indexes.base.Index:
        if isinstance(pd_obj, pd.Series):
            return pd_obj.name

        return pd_obj.columns

    return cols


@pd.api.extensions.register_dataframe_accessor("dropinf")
@pd.api.extensions.register_series_accessor("dropinf")
def DropInfAccessor(pd_obj: Pd) -> Callable[[bool], Pd | None]:
    def dropinf(inplace: bool = False) -> Pd | None:
        mask = ~pd_obj.isin([inf, -inf])
        if isinstance(pd_obj, pd.DataFrame):
            mask = mask.all(axis=1)

        result = pd_obj[mask]

        if inplace:
            pd_obj._update_inplace(result)
            return None

        return result

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
