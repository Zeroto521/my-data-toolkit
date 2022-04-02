from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr


@register_series_method
def values_to_dict(s: pd.Series) -> dict[IntOrStr, list[IntOrStr]]:
    """
    Convert :attr:`~pandas.Series.index` and :attr:`~pandas.Series.values` to
    :class:`dict`.

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
    """

    return {key: s[s.index == key].to_list() for key in s.index.unique()}
