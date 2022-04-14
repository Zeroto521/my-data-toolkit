from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.util._decorator import warning


if TYPE_CHECKING:
    from dtoolkit._typing import IntOrStr


@register_dataframe_method
@warning(
    "'dtoolkit.accessor.dataframe.unique_counts' is deprecated and will be removed in"
    "0.0.15. Please use 'pd.DataFrame.nunique' instead. "
    "(Warning added DToolKit 0.0.14)",
    DeprecationWarning,
    stacklevel=3,
)
def unique_counts(
    df: pd.DataFrame,
    axis: IntOrStr = 0,
    dropna: bool = True,
) -> pd.Series:
    """
    Count unique values for each column or row.

    .. warning::
        ``dtoolkit.accessor.dataframe.unique_counts`` is deprecated and will be removed
        in 0.0.15. Please use :meth:`pandas.DataFrame.nunique` instead.
        (Warning added DToolKit 0.0.14)

    Parameters
    ----------
    axis : {0 or 'index', 1 or 'columns'}, default 0
        - If 0 or 'index' counts are generated for each column.
        - If 1 or 'columns' counts are generated for each row.

    dropna : bool, default True
        Don't include NaN in the counts.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 1, 2], "b": [1, 3, 4]})
    >>> df
       a  b
    0  1  1
    1  1  3
    2  2  4
    >>> df.unique_counts()
    a    2
    b    3
    dtype: int64
    >>> df.unique_counts(1)
    0    1
    1    2
    2    2
    dtype: int64
    """

    return df.nunique(axis=axis, dropna=dropna)
