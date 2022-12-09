from __future__ import annotations

from functools import lru_cache
from typing import Callable
from warnings import warn

import pandas as pd
from pandas.api.types import is_list_like
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def textdistance(
    s: pd.Series,
    /,
    other: str | pd.Series,
    method: Callable = None,
    align: bool = True,
    **kwargs,
) -> pd.Series:
    """
    Return a ``Series`` containing the text distance to aligned ``other``.

    Parameters
    ----------
    other : None, str or Series

    align : bool, default True
        If True, automatically aligns GeoSeries based on their indices. If False,
        the order of elements is preserved.

    method : Callable, default None
        The method to calculate the distance. The first and second positional parameters
        will be compared. If None, :meth:`rapidfuzz.fuzz.ratio`. Recommended use methods
        in :mod:`rapidfuzz.fuzz`, :mod:`rapidfuzz.string_metric`, and
        :mod:`rapidfuzz.distance`.

    **kwargs
        Additional keyword arguments passed to ``method``.

    Returns
    -------
    Series
        The values are the text distances.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'rapidfuzz'.

    TypeError
        - If ``s`` is not string dtype.
        - If ``other`` is not string dtype.

    ValueError
        If ``other``'s length is not equal to the length of ``s``.

    See Also
    --------
    rapidfuzz.fuzz
    rapidfuzz.string_metric
    rapidfuzz.distance
    textdistance_matrix

    Notes
    -----
    The result of comparing to None or nan value is depended on the ``method``.

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])
    >>> s
    0    hello
    1    world
    dtype: object
    >>> s.textdistance("python")
    0    36.363636
    1    18.181818
    dtype: float64
    >>> s.textdistance(pd.Series(["hello", "python"]))
    0    100.000000
    1     18.181818
    dtype: float64
    """

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if method is None:
        method = __import__("rapidfuzz").fuzz.ratio
    method = lru_cache(method)

    if (
        isinstance(other, str)
        or other is None
        or (not is_list_like(other) and pd.isna(other))
    ):
        return s.apply(method, args=(other,), **kwargs)

    elif isinstance(other, pd.Series):
        if not is_string_dtype(other):
            raise TypeError(f"Expected Series(string), but got {other.dtype!r}.")

        if align and not s.index.equals(other.index):
            warn("The indices are different.", stacklevel=find_stack_level())
            s, other = s.align(other)

        if s.size != other.size:
            raise ValueError(f"{s.size=} != {other.size=}.")

        return pd.Series(
            (method(*xy, **kwargs) for xy in zip(s, other)),
            name=s.name,
            index=s.index,
        )

    raise TypeError(f"Expected Series(string), but got {type(other).__name__!r}.")
