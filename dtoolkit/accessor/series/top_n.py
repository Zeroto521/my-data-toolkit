from __future__ import annotations

from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method("topn")
@register_series_method
def top_n(
    s: pd.Series,
    /,
    n: int = 5,
    largest: bool = True,
    keep: Literal["first", "last", "all"] = "first",
) -> pd.Series:
    """
    Return the top `n` values.

    A sugary syntax wraps :meth:`~pandas.Series.nlargest` and
    :meth:`~pandas.Series.nsmallest` methods.

    Parameters
    ----------
    n : int, default 5
        Number of top to return.

    largest : bool, default True
        - True, the top is the largest.
        - True, the top is the smallest.

    keep : {"first", "last", "all"}, default "first"
        Where there are duplicate values:

        - first : prioritize the first occurrence(s).
        - last : prioritize the last occurrence(s).
        - all : do not drop any duplicates, even it means selecting more than
          n items.

    Returns
    -------
    Series

    See Also
    --------
    dtoolkit.accessor.series.expand
        Transform each element of a list-like to a column.

    dtoolkit.accessor.dataframe.top_n
        Returns each row's top n.
    """

    if largest:
        return s.nlargest(n=n, keep=keep)

    return s.nsmallest(n=n, keep=keep)
