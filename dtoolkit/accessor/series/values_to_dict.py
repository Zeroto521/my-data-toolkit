from __future__ import annotations

import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.dropna_index import dropna_index


@register_series_method
def values_to_dict(
    s: pd.Series,
    /,
    unique: bool = True,
    to_list: bool = True,
    dropna: bool = True,
) -> dict:
    """
    Convert :attr:`~pandas.Series.index` and :attr:`~pandas.Series.values` to
    :class:`dict`.

    Parameters
    ----------
    unique : bool, default True
        If True would drop duplicate elements.

    to_list : bool, default True
        If True one element value will return :class:`list`.

    dropna : bool, default True
        If True it will drop the ``nan`` value whatever it's key or value.

    Returns
    -------
    dict
        The datastruct is ``{index: [values]}``.

    See Also
    --------
    pandas.Series.to_dict
    dtoolkit.accessor.dataframe.values_to_dict

    Notes
    -----
    The same key of values would be merged into :class:`list`.

    Examples
    --------
    >>> import json
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(range(4), index=["a", "b", "a", "c"])
    >>> s
    a    0
    b    1
    a    2
    c    3
    dtype: int64
    >>> print(json.dumps(s.values_to_dict(), indent=4))
    {
        "a": [
            0,
            2
        ],
        "b": [
            1
        ],
        "c": [
            3
        ]
    }

    Unpack one element value list.

    >>> print(json.dumps(s.values_to_dict(to_list=False), indent=4))
    {
        "a": [
            0,
            2
        ],
        "b": 1,
        "c": 3
    }
    """

    if dropna:
        # Drop NA both index and values
        s = dropna_index(s.dropna())

    if s.empty:
        return {}

    return {
        key: handle_element(s[s.index == key], unique=unique, to_list=to_list)
        for key in s.index.unique()
    }


def handle_element(s: pd.Series, /, unique: bool, to_list: bool):
    if unique:
        s = s.unique()

    s = s.tolist()
    # Unfold one element list-like
    return s[0] if not to_list and len(s) == 1 else s
