from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr


@register_series_method
def values_to_dict(
    s: pd.Series,
    to_list: bool = True,
) -> dict[IntOrStr, list[IntOrStr] | IntOrStr]:
    """
    Convert :attr:`~pandas.Series.index` and :attr:`~pandas.Series.values` to
    :class:`dict`.

    Parameters
    ----------
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
        key: unpack_list(
            s[s.index == key].to_list(),
            to_list=to_list,
        )
        for key in s.index.unique()
    }


def unpack_list(array: list, to_list: bool = True) -> list[IntOrStr] | IntOrStr:
    # unfold one element list

    if not to_list and len(array) == 1:
        return array[0]

    return array
