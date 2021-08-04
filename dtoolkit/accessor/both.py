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
    """

    def __call__(self) -> str | list[str]:
        if isinstance(self.pd_obj, pd.Series):
            return self.pd_obj.name

        return self.pd_obj.columns.tolist()
