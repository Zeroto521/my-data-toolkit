from __future__ import annotations

from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import top_n as s_top_n


@register_dataframe_method("topn")
@register_dataframe_method
def top_n(
    df: pd.DataFrame,
    /,
    n: int = 5,
    largest: bool = True,
    keep: Literal["first", "last", "all"] = "first",
    prefix: str = "top",
    delimiter: str = "_",
    element: Literal["index", "value", "both"] = "index",
) -> pd.DataFrame:
    """
    Returns each row's top `n`.

    Parameters
    ----------
    n : int, default 5
        Number of top to return.

    largest : bool, default True
        - True, the top is the largest.
        - False, the top is the smallest.

    keep : {"first", "last", "all"}, default "first"
        Where there are duplicate values:

        - first : prioritize the first occurrence(s).
        - last : prioritize the last occurrence(s).
        - all : do not drop any duplicates, even it means selecting more than
          n items.

    prefix : str, default "top"
        The prefix name of the new DataFrame column.

    delimiter : str, default "_"
        The delimiter between `prefix` and number.

    element : {"index", "value", "both"}, default "index"
        To control the structure of return dataframe value.

        - index: the structure of value is only ``{column index}``.
        - value: the structure of value is only ``{value}``.
        - both: the structure of value is ``({column index}, {value})``.

    Returns
    -------
    DataFrame
        - The structure of column name is ``{prefix}{delimiter}{number}``.
        - The default structure of value is ``{column index}`` and could be
          controlled via ``element``.

    Raises
    ------
    ValueError
        If ``element`` isn't "both", "index" or "value".

    See Also
    --------
    dtoolkit.accessor.dataframe.expand
        Transform each element of a list-like to a column.

    Notes
    -----
    - This method could be called via ``df.top_n`` or ``df.topn``.

    - Q & A
        Q: Any different to :meth:`~pandas.DataFrame.nlargest` and
        :meth:`~pandas.DataFrame.nsmallest`?

        A: :meth:`~pandas.DataFrame.nlargest` and
        :meth:`~pandas.DataFrame.nsmallest` base one column to return all selected
        columns dataframe top `n`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "a": [1, 3, 2, 1],
    ...         "b": [3, 2, 1, 1],
    ...         "c": [2, 1, 3, 1],
    ...     },
    ... )
    >>> df
       a  b  c
    0  1  3  2
    1  3  2  1
    2  2  1  3
    3  1  1  1

    Get each row's largest top **2**, sorts values and returns index.

    >>> df.top_n(2)
        top_1   top_2
    0       b       c
    1       a       b
    2       c       a
    3       a       b

    Get each row's largest top **2**, sorts values and returns values.

    >>> df.top_n(2, element="value")
       top_1  top_2
    0      3      2
    1      3      2
    2      3      2
    3      1      1

    Get each row's both **index** and **value** of largest top 2, sorts values
    and return both index and values.

    >>> df.top_n(2, element="both")
        top_1   top_2
    0  (b, 3)  (c, 2)
    1  (a, 3)  (b, 2)
    2  (c, 3)  (a, 2)
    3  (a, 1)  (b, 1)

    Get each row's smallest top **1** and **keep** the duplicated values.

    >>> df.top_n(1, largest=False, keep="all")
        top_1   top_2   top_3
    0       a     NaN     NaN
    1       c     NaN     NaN
    2       b     NaN     NaN
    3       a       b       c
    """

    def wrap_s_top_n(s: pd.Series) -> pd.Series:
        top = s_top_n(s, n=n, largest=largest, keep=keep)

        if element == "index":
            data = top.index
        elif element == "value":
            data = top.values
        elif element == "both":
            data = zip(top.index, top.values)
        else:
            raise ValueError('element must be either "both", "index" or "value"')

        return pd.Series(data, index=pd.RangeIndex(1, top.size + 1))

    return df.apply(wrap_s_top_n, axis=1).add_prefix(prefix + delimiter)
