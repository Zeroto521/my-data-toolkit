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
    s: pd.Series,
    /,
    other: str | list | np.ndarray | pd.Series,
    method: Callable = None,
    align: bool = True,
) -> pd.Series:
    """
    Return a ``Series`` containing the text distance to aligned ``other``.

    Parameters
    ----------
    other : str, list, ndarray, or Series

    align : bool, default True
        If True, automatically aligns GeoSeries based on their indices. If False,
        the order of elements is preserved.

    method : Callable, default None
        The method to calculate the distance. If None, use
        `thefuzz.fuzz.ratio <https://github.com/seatgeek/thefuzz>`_.

    Returns
    -------
    Series
        The values are the text distances.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'thefuzz'.

    TypeError
        - If ``s`` is not string dtype.
        - If ``other`` is not string dtype.

    ValueError
        - If ``other`` is list-like but its length is not equal to the length of ``s``.
        - If ``other`` is list-like but it is not 1-dimensional.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])
    >>> s
    0    hello
    1    world
    dtype: object
    >>> s.textdistance("python")
    0    36
    1    18
    dtype: int64
    >>> s.textdistance(["hello", "python"])
    0    100
    1     18
    dtype: int64
    """

    if method is None:
        method = __import__("thefuzz.fuzz").fuzz.ratio

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if isinstance(other, str) or other is None:
        return s.apply(method, args=(other,))

    elif is_list_like(other):
        if len(other) != s.size:
            raise ValueError(f"{len(other)=} != {s.size=}.")
        if isinstance(other, pd.Series) and align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        return pd.Series(
            (method(*x) for x in zip(s, validate_string_dtype(other))),
            name=s.name,
            index=s.index,
        )

    raise TypeError(f"Unknown type: {type(other).__name__!r}.")


def validate_string_dtype(other: list | np.ndarray | pd.Series) -> np.ndarray:
    other = np.asarray(other)
    if other.ndim != 1:
        raise ValueError("'other' must be 1-dimensional.")
    if not is_string_dtype(other):
        raise TypeError(f"Expected string dtype, but got {other.dtype!r}.")

    return other
