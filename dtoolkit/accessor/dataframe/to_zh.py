from typing import Hashable

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series.to_zh import LOCALIZATION
from dtoolkit.accessor.series.to_zh import to_zh as s_to_zh


@register_dataframe_method
def to_zh(
    df: pd.DataFrame,
    /,
    column: Hashable,
    *,
    locale: LOCALIZATION = "zh-cn",
    dictionary: dict = None,
) -> pd.DataFrame:
    """
    Simple conversion and localization between simplified and traditional Chinese.

    Parameters
    ----------
    column : Hashable
        The column to convert.

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
    dtoolkit.accessor.series.to_zh

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> df = pd.DataFrame({'zh': ['漢', '字']})
    >>> df
       zh
    0  漢
    1  字
    >>> df.to_zh('zh')
       zh
    0  汉
    1  字
    """

    return df.assign(
        **{
            column: s_to_zh(
                df[column],
                locale=locale,
                dictionary=dictionary,
            ),
        },
    )
