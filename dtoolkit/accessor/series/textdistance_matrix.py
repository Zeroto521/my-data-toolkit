from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.textdistance import textdistance
from dtoolkit.accessor.series.textdistance import validate_string_dtype


@register_series_method
def textdistance_matrix(
    s: gpd.GeoSeries,
    /,
    other: None | list | np.ndarray | pd.Series = None,
    method: Callable = None,
) -> pd.DataFrame:
    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if other is None:
        other = s.copy()
    if not is_list_like(other):
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")
    if len(other) != s.size:
        raise ValueError(f"{len(other)=} != {s.size=}.")

    func = lambda o: textdistance(s, o, method=method)
    res = pd.concat(map(func, validate_string_dtype(other)), axis=1)
    return res.set_axis(other.index, axis=1) if isinstance(other, pd.Series) else res
