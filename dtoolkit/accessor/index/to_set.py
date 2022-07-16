from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit.accessor.register import register_index_method


@register_index_method
def to_set(index: pd.Index, /, level: int | Hashable = None) -> set:
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
    dtoolkit.accessor.series.to_set

    Notes
    -----
    Different to :meth:`~pandas.Index.unique`, it returns :class:`~pandas.Index`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> index = pd.Index([1, 2, 2])
    >>> index
    Int64Index([1, 2, 2], dtype='int64')
    >>> index.to_set()
    {1, 2}
    >>> index = pd.MultiIndex.from_arrays(
    ...     [
    ...         [1, 1, 2, 2],
    ...         ['red', 'blue', 'red', 'blue'],
    ...     ],
    ...     names=['number', 'color'],
    ... )
    >>> index
    MultiIndex([(1,  'red'),
                (1, 'blue'),
                (2,  'red'),
                (2, 'blue')],
               names=['number', 'color'])
    >>> index.to_set(0)
    {1, 2}
    >>> index.to_set('number')
    {1, 2}
    """

    return set(index.unique(level=level))
