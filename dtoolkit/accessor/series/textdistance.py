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
    other: None | str | pd.Series = None,
    method: Callable = None,
    align: bool = True,
) -> pd.Series:
    """
    Return a ``Series`` containing the text distance to aligned ``other``.

    Parameters
    ----------
    other : None, str or Series
        If None, the text distance is 0.

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

    See Also
    --------
    textdistance_matrix

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
    >>> s.textdistance(pd.Series(["hello", "python"]))
    0    100
    1     18
    dtype: int64
    """

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if method is None:
        method = __import__("thefuzz.fuzz").fuzz.ratio

    if isinstance(other, str) or other is None:
        return s.apply(method, args=(other,))

    elif isinstance(other, pd.Series):
        if not is_string_dtype(other):
            raise TypeError(f"Expected string dtype, but got {other.dtype!r}.")

        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        if s.size != other.size:
            raise ValueError(f"{s.size=} != {other.size=}.")

        return pd.Series(
            (method(*xy) for xy in zip(s, other)),
            name=s.name,
            index=s.index,
        )

    raise TypeError(f"Unknown type: {type(other).__name__!r}.")
