from __future__ import annotations

import pandas as pd
from pandas.api.types import is_number

from dtoolkit.accessor.register import register_series_method


@register_series_method
def len(s: pd.Series, /, number: int = 1, other: int = None) -> pd.Series:
    """
    Return the length of each element in the series.

    Equals to ``s.apply(len)``, but the length of ``number`` type will as ``1``,
    the length of other types will as ``NaN``.

    Parameters
    ----------
    number : int, default 1
        The default length of `number` type.

    other : int or None, default None
        The default length of `other` type.

    Returns
    -------
    Series

    Notes
    -----
    - To keep the Python naming style, so use this accessor via
      ``Series.len`` rather than ``Series.lens``.

    - Different to :meth:`pandas.Series.str.len`. It only returns
      :class:`collections.abc.Iterable` type length. Other type will return `NaN`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([0, 1, 1.5, "string", ("tuple",), ["list"], {}, object])
    >>> s
    0                   0
    1                   1
    2                 1.5
    3              string
    4            (tuple,)
    5              [list]
    6                  {}
    7    <class 'object'>
    dtype: object
    >>> s.len()
    0    1.0
    1    1.0
    2    1.0
    3    6.0
    4    1.0
    5    1.0
    6    0.0
    7    NaN
    dtype: float64

    Set `number` and `other` default return.

    >>> s.len(number=0, other=0)
    0    0
    1    0
    2    0
    3    6
    4    1
    5    1
    6    0
    7    0
    dtype: int64
    """

    return s.apply(_wrap_len, number=number, other=other)


def _wrap_len(x, number: int, other: int | None) -> int | None:
    if hasattr(x, "__len__"):
        return x.__len__()
    elif is_number(x):
        return number

    return other
