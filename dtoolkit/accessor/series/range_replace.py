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
) -> pd.Series:
    if not is_dict_like(to_replace):
        raise TypeError(
            "Expecting 'to_replace' to be a dict, got invalid type "
            f"{type(to_replace).__name__!r}",
        )

    for left_right, value in to_replace.items():
        if not (is_list_like(left_right) and len(left_right) == 2):
            raise ValueError(
                "The key of dict should be a range type contains scalar element, "
                "the first element must be greater than the second one",
            )

        s = between_replace(s, *left_right, value, inclusive=inclusive)

    return s
