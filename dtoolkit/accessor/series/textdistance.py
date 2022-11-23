from __future__ import annotations

from functools import wraps
from functools import lru_cache

from typing import Callable
from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_list_like

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def textdistance(
    s: pd.Series,
    /,
    other: None | str | pd.Series = None,
    method: Callable = None,
    align: bool = True,
    enable_checking: bool = True,
    enable_cache: bool = True,
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

    enable_checking : bool, default True
        If True, check the input. If the input is None, nan or empty string the result
        will be 0.

    enable_cache : bool, default True
        If True, cache the result. The text distance algorithm is hrad to be vectorized,
        and it's a time-consuming operation. Cache the result can speed up the process.

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
        If ``other``'s length is not equal to the length of ``s``.

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
    if enable_checking:
        method = check(method)
    if enable_cache:
        method = lru_cache(method)

    if isinstance(other, str):
        return s.apply(method, args=(other,))
    elif isinstance(other, pd.Series):
        if not is_string_dtype(other):
            raise TypeError(f"Expected Series(string), but got {other.dtype!r}.")

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
    elif other is None or (not is_list_like(other) and pd.isna(other)):
        # NOTE:
        # - pd.na(Series) returns array-like of bool
        #   to make sure pd.isna(other) returns bool
        #   need to other is not array-like
        # - compare to None or nan always returns 0
        #   the behavior is following thefuzz.fuzz.ratio
        return pd.Series(np.zeros(s.size), name=s.name, index=s.index)

    raise TypeError(f"Expected Series(string), but got {type(other).__name__!r}.")


def check_none(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # NOTE: compare to None always returns 0
        # the behavior is following thefuzz.fuzz.ratio
        return 0 if args[0] is None or args[1] is None else func(*args, **kwargs)

    return decorator


def check_nan(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # NOTE: compare to nan always returns 0
        # the behavior is following thefuzz.fuzz.ratio
        return 0 if pd.isna(args[0]) or pd.isna(args[1]) else func(*args, **kwargs)

    return decorator


def check_empty_string(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # NOTE: compare to empty string always returns 0
        # the behavior is following thefuzz.fuzz.ratio
        return 0 if len(args[0]) == 0 or len(args[1]) == 0 else func(*args, **kwargs)

    return decorator


def check(func):
    @wraps(func)
    @check_none
    @check_nan
    @check_empty_string
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return decorator
