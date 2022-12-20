from __future__ import annotations

from functools import partial

import pandas as pd
from pandas.api.types import is_number

from dtoolkit.accessor.register import register_index_method


@register_index_method
def len(index: pd.Index, /, number: int = 1, other: int = None) -> pd.Index:
    """
    Return the length of each element in the Index.

    Equals to ``index.map(len)``, but the length of ``number`` type will as ``1``,
    the length of other types will as ``NaN``.

    Parameters
    ----------
    number : int, default 1
        The default length of `number` type.

    other : int or None, default None
        The default length of `other` type.

    Returns
    -------
    Index(int64)

    See Also
    --------
    dtoolkit.accessor.series.len

    Notes
    -----
    - To keep the Python naming style, so use this accessor via ``Index.len``
      rather than ``Index.lens``.

    - Different to :meth:`pandas.Index.str.len`. It only returns
      :class:`collections.abc.Iterable` type length. Other type will return `NaN`.

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> index = pd.Index([0, 1.5, "str", ("tuple",), ["list"], {}, object])
    >>> index
    Index([0, 1.5, 'str', ('tuple',), ['list'], {}, <class 'object'>], dtype='object')
    >>> index.len()
    Float64Index([1.0, 1.0, 3.0, 1.0, 1.0, 0.0, nan], dtype='float64')

    Set `number` and `other` default return.

    >>> index.len(number=0, other=0)
    Int64Index([0, 0, 3, 1, 1, 0, 0], dtype='int64')
    """

    return index.map(partial(length, number=number, other=other))


def length(x, number: int, other: int | None) -> int | None:
    if hasattr(x, "__len__"):
        return x.__len__()
    elif is_number(x):
        return number

    return other
