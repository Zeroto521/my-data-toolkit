from __future__ import annotations

import pandas as pd
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor.register import register_series_method


@register_series_method
def bin(s: pd.Series, bins, **kwargs) -> pd.Series:
    """
    Bin values into discrete intervals.

    Parameters
    ----------
    bins : int, sequence of scalars, or IntervalIndex
        The criteria to bin by.

        - int : Defines the number of equal-width bins in the range of x.
         The range of x is extended by .1% on each side to include the minimum and
         maximum values of x.

        - sequence of scalars : Defines the bin edges allowing for non-uniform width.
         No extension of the range of x is done.

        - IntervalIndex : Defines the exact bins to be used. Note that IntervalIndex
         for bins must be non-overlapping.

    Returns
    -------
    Series

    See Also
    --------
    pandas.cut: This accessor's prototype method.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    Create **score** samples:

    >>> s = pd.Series([100, 10, 50, 20, 90, 60])

    Bin score to rank level:

        - (0, 60] -> E
        - (60, 70] -> D
        - (70, 80] -> C
        - (80, 90] -> B
        - (90, 100] -> A

    >>> s.bin([0, 60, 70, 80, 90, 100], labels=['E', 'D', 'C', 'B', 'A'], right=True)
    0    A
    1    E
    2    E
    3    E
    4    B
    5    E
    dtype: category
    Categories (5, object): ['E' < 'D' < 'C' < 'B' < 'A']
    """

    return pd.cut(s, bins, **kwargs)
