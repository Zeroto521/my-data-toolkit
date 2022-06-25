from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit.accessor.register import register_index_method


@register_index_method
def to_set(index: pd.Index, level: int | Hashable = None) -> set:
    """
    Return a :keyword:`set` of the values.

    A sugary syntax wraps :keyword:`set`::

        set(index)

    Parameters
    ----------
    level : int or Hashable, optional
        Only return values from specified level (for :class:`~pandas.MultiIndex`).
        If int, gets the level by integer position, else by level name.

    Returns
    -------
    set

    See Also
    --------
    pandas.Index.unique

    Notes
    -----
    Different to :meth:`~pandas.Index.unique`, it returns :class:`~pandas.Index`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> i = pd.Index([1, 2, 2])
    >>> i
    Int64Index([1, 2, 2], dtype='int64')
    >>> i.to_set()
    {1, 2}
    """

    return set(index.unique(level=level))
