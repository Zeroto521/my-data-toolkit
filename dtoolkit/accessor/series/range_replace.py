from __future__ import annotations

from typing import Literal

import pandas as pd
from pandas.api.types import is_dict_like
from pandas.api.types import is_list_like

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.between_replace import between_replace


@register_series_method
def range_replace(
    s: pd.Series,
    /,
    to_replace: dict,
    inclusive: Literal["both", "neither", "left", "right"] = "both",
    limit: int = None,
    regex: bool = False,
    method: Literal["pad", "ffill", "bfill"] = None,
) -> pd.Series:
    if not is_dict_like(to_replace):
        raise TypeError(
            "Expecting 'to_replace' to be a dict, got invalid type "
            f"{type(to_replace).__name__!r}",
        )

    for key, value in to_replace.items():
        if is_list_like(key) and len(key) == 2 and key[0] < key[1]:
            s = between_replace(s, *key, value, inclusive=inclusive)
        else:
            s = s.replace(key, value, limit=limit, regex=regex, method=method)

    return s
