from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr


@register_dataframe_method
def cols(df: pd.DataFrame) -> list[IntOrStr]:
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.

    Returns
    -------
    list of str or int
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

    >>> d = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}})
    >>> d.cols()
    ['a', 'b']
    """

    return df.columns.tolist()
