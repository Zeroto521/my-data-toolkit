from __future__ import annotations

import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from .base import Accessor


@register_dataframe_accessor("cols")
@register_series_accessor("cols")
class ColumnAccessor(Accessor):
    """
    A API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.

    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns

    Examples
    --------
    >>> from dtoolkit.accessor import ColumnAccessor
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

    def __call__(self) -> str | list[str]:
        if isinstance(self.pd_obj, pd.Series):
            return self.pd_obj.name

        return self.pd_obj.columns.tolist()
