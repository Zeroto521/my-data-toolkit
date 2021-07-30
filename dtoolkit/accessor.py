from __future__ import annotations

import pandas as pd
from numpy import inf

from ._typing import Pd


__all__ = [
    "ColumnAccessor",
    "DropInfAccessor",
    "FilterInAccessor",
]


class Accessor:
    def __init__(self, pd_obj: Pd):
        self.pd_obj = pd_obj


@pd.api.extensions.register_dataframe_accessor("cols")
@pd.api.extensions.register_series_accessor("cols")
class ColumnAccessor(Accessor):
    def __call__(self) -> str | list[str]:
        if isinstance(self.pd_obj, pd.Series):
            return self.pd_obj.name

        return self.pd_obj.columns.tolist()


@pd.api.extensions.register_dataframe_accessor("dropinf")
@pd.api.extensions.register_series_accessor("dropinf")
class DropInfAccessor(Accessor):
    def __call__(self, inplace: bool = False) -> Pd | None:
        mask = ~self.pd_obj.isin([inf, -inf])
        if isinstance(self.pd_obj, pd.DataFrame):
            mask = mask.all(axis=1)

        result = self.pd_obj[mask]

        if inplace:
            self.pd_obj._update_inplace(result)
            return None

        return result


@pd.api.extensions.register_dataframe_accessor("filterin")
class FilterInAccessor(Accessor):
    def __call__(
        self,
        cond: dict[str, list[str]],
        inplace: bool = False,
    ) -> pd.DataFrame | None:
        mask_all = self.pd_obj.isin(cond)
        mask_selected = mask_all[cond.keys()]
        result = self.pd_obj[mask_selected.all(axis=1)]

        if inplace:
            self.pd_obj._update_inplace(result)
            return None

        return result
