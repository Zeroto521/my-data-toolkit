from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def cols(df: pd.DataFrame, /, to_list: bool = False) -> list[Hashable]:
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.

    Parameters
    ----------
    to_list : bool, default False
        This option doesn't work, and it's used to fit
        :func:`dtoolkit.accessor.series.cols` arguments.

    Returns
    -------
    list of Hashable
        The column names.

    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns
    dtoolkit.accessor.series.cols
    dtoolkit.accessor.dataframe.cols

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    Get :attr:`~pandas.Series.name`.

    >>> s = pd.Series(range(10), name="item")
    >>> s.cols()
    'item'

    Get :attr:`~pandas.DataFrame.columns`.

    >>> d = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> d.cols()
    ['a', 'b']
    """

    return df.columns.tolist()
