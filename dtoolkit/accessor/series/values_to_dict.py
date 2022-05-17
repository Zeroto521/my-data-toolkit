from __future__ import annotations

import pandas as pd

from dtoolkit.accessor.register import register_series_method  # noqa


@register_series_method
def values_to_dict(s: pd.Series, unique: bool = True, to_list: bool = True) -> dict:
    """
    Convert :attr:`~pandas.Series.index` and :attr:`~pandas.Series.values` to
    :class:`dict`.

    Parameters
    ----------
    unique : bool, default True
        If True would drop duplicate elements.

    to_list : bool, default True
        If True one element value will return :keyword:`list`.

    Returns
    -------
    dict
        The datastruct is ``{index: [values]}``.

    See Also
    --------
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

    return {
        key: s.loc[s.index == key].pipe(
            handle_element,
            unique=unique,
            to_list=to_list,
        )
        for key in s.index.unique()
    }


def handle_element(s: pd.Series, unique: bool = False, to_list: bool = True):
    if unique:
        s = s.unique()

    s = s.tolist()
    if not to_list and len(s) == 1:
        # Unfold one element list-like
        return s[0]

    return s
