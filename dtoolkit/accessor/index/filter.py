from __future__ import annotations

from re import compile

import pandas as pd
from pandas.core.common import count_not_none
from pandas.core.dtypes.common import ensure_str

from dtoolkit.accessor.register import register_index_method


@register_index_method
def filter(
    index: pd.Index,
    /,
    items=None,
    like: str | None = None,
    regex: str | None = None,
    complement: bool = False,
) -> pd.Index:
    """
    Subset the Index according to the specified labels.

    Parameters
    ----------
    items : list-like
        Keep labels from axis which are in items.

    like : str
        Keep labels from axis for which "like in label == True".

    regex : str (regular expression)
        Keep labels from axis for which ``re.search(regex, label) == True``.

    complement : bool, default False
        If True, return the complement of the result.

    Returns
    -------
    Index

    See Also
    --------
    pandas.Series.filter
    pandas.DataFrame.filter

    Notes
    -----
    The ``items``, ``like``, and ``regex`` parameters are enforced to be mutually
    exclusive.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> index = pd.Index(['one', 'two', 'three'])
    >>> index
    Index(['one', 'two', 'three'], dtype='object')

    Select by name.

    >>> index.filter(items=['one', 'three'])
    Index(['one', 'three'], dtype='object')

    Select by regular expression.

    >>> index.filter(regex='e$')
    Index(['one', 'three'], dtype='object')

    Doesn't select containing 't'.
    >>> index.filter(like='t', complement=True)
    Index(['one'], dtype='object')
    """

    if count_not_none(items, like, regex) > 1:
        raise TypeError(
            "Keyword arguments `items`, `like`, or `regex` are mutually exclusive.",
        )

    if items:
        choice = lambda x: x not in items if complement else x in items  # noqa: E731
        return index.reindex(i in index for i in items if choice(i))[0]
    elif like:
        condition = index.map(lambda x: like in ensure_str(x))
    elif regex:
        searcher = compile(regex).search
        condition = index.map(lambda x: searcher(ensure_str(x)) is not None)
    else:
        raise TypeError("Must pass either `items`, `like`, or `regex`.")

    return index[~condition if complement else condition]
