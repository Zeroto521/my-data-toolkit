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
    s: pd.Series,
    /,
    other: None | list | np.ndarray | pd.Series = None,
    method: Callable = None,
) -> pd.DataFrame:
    """
    Returns a ``DataFrame`` containing the text distances matrix between in ``s``
    and ``other``.

    Parameters
    ----------
    other : None, list, ndarray, or Series, default None
        If None, use ``s``.

    method : Callable, default None
        The method to calculate the distance. If None, use ``thefuzz.fuzz.ratio``.

    Returns
    -------
    DataFrame
        The values are the text distances.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'thefuzz'.

    TypeError
        - If ``s`` is not string dtype.
        - If ``other`` is not string dtype.

    ValueError
        If ``other`` but it is not 1-dimensional.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])
    >>> s
    0    hello
    1    world
    dtype: object
    >>> s.textdistance_matrix(["hello", "python"])
         0   1
    0  100  36
    1   20  18
    """

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    if other is None:
        other = s.copy()
    if not is_list_like(other):
        raise TypeError(f"Unknown type: {type(other).__name__!r}.")

    data = (textdistance(s, o, method=method) for o in validate_string_dtype(other))
    res = pd.concat(data, axis=1)
    return res.set_axis(other.index, axis=1) if isinstance(other, pd.Series) else res
