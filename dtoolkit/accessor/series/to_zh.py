from typing import Literal

import pandas as pd
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method


LOCALIZATION = Literal[
    "zh-hans",
    "zh-hant",
    "zh-cn",
    "zh-sg",
    "zh-tw",
    "zh-hk",
    "zh-my",
    "zh-mo",
]


@register_series_method
def to_zh(
    s: pd.Series,
    /,
    *,
    locale: LOCALIZATION = "zh-cn",
    dictionary: dict = None,
) -> pd.Series:
    """
    Simple conversion and localization between simplified and traditional Chinese.

    Parameters
    ----------
    locale : {"zh-hans", "zh-hant", "zh-cn", "zh-sg", "zh-tw", "zh-hk", "zh-my", \
"zh-mo"}, default "zh-cn"
        Locale to convert to.

    dictionary : dict, default None
        A dictionary which updates the conversion table, eg.
        ``{'from1': 'to1', 'from2': 'to2'}``

    Returns
    -------
    Series(string)

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'zhconv'.

    TypeError
        If ``s`` is not string dtype.

    See Also
    --------
    dtoolkit.accessor.dataframe.to_zh

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series(['漢', '字'])
    >>> s
    0    漢
    1    字
    dtype: object
    >>> s.to_zh(locale="zh-cn")
    0    汉
    1    字
    dtype: object
    """

    from zhconv import convert

    if not is_string_dtype(s):
        raise TypeError(f"Expected string dtype, but got {s.dtype!r}.")

    return s.apply(convert, locale=locale, update=dictionary)
