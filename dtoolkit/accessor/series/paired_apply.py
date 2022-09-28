from __future__ import annotations

from typing import Callable
from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def paired_apply(
    s,
    /,
    other,
    func: Callable,
    align: bool = True,
    required_1d: bool = True,
    *args,
    **kwargs,
) -> pd.Series:
    if not is_list_like(other):
        return s.apply(func, args=(other, *args), **kwargs)

    if len(other) != s.size:
        raise ValueError(f"{len(other)=} != {s.size=}.")
    if isinstance(other, pd.Series) and align and not s.index.equals(other.index):
        warn("The indices are different.", stacklevel=find_stack_level())
        s, other = s.align(other)

    other = np.asarray(other)
    if required_1d and other.ndim != 1:
        raise ValueError("'other' must be 1-dimensional.")

    func = lambda x: func(*x, *args, **kwargs)
    return pd.Series(map(func, zip(s, other)), name=s.name, index=s.index)
