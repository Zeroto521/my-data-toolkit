from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def cols(
    s: pd.Series,
    /,
    to_list: bool = False,
) -> Hashable | None | list[Hashable | None]:
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.

    Parameters
    ----------
    to_list : bool, default False
        If True, return a list type.

    Returns
    -------
    Hashable, None or list of them
        The name of the Series.

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
    >>> s.cols(to_list=True)
    ['item']

    Get :attr:`~pandas.DataFrame.columns`.

    >>> d = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> d.cols()
    ['a', 'b']
    """

    return [s.name] if to_list else s.name
