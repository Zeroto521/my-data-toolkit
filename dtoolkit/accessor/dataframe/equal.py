from __future__ import annotations
from typing import Any
import pandas as pd
import numpy as np
from warnings import warn
from pandas.api.types import is_array_like
from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def equal(
    df: pd.DataFrame,
    /,
    other: Any | list | np.ndarray | pd.Series,
    align: bool = True,
    **kwargs,
) -> pd.DataFrame:
    if is_array_like(other):
        if align and isinstance(other, pd.Series) and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        other = np.asarray(other)
        if other.ndims != 1:
            ...

        other = other.reshape(-1, 1)

    return pd.Series(np.equal(s, other, **kwargs), index=s.index)
