from __future__ import annotations

from typing import Callable
from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def textdistance(
    s,
    /,
    other: str | list | np.ndarray | pd.Series,
    method: Callable = None,
    align: bool = True,
) -> pd.Series:
    if method is None:
        method = __import__("thefuzz.fuzz").fuzz.ratio

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if isinstance(other, str):
        return s.apply(ratio, args=(other,))

    elif is_list_like(other):
        if len(other) != s.size:
            raise ValueError(f"{len(other)=} != {s.size=}.")
        if isinstance(other, pd.Series) and align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        other = np.asarray(other)
        if other.ndim != 1:
            raise ValueError("'other' must be 1-dimensional.")
        if not is_string_dtype(other):
            raise TypeError(f"Expected string dtype, but got {other.dtype!r}.")

        method = lambda x: method(*x)
        return pd.Series(map(method, zip(s, other)), name=s.name, index=s.index)

    else:
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")
