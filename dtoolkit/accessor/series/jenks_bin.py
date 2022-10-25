import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.jenks_breaks import jenks_breaks


@register_series_method("jenks_cut")
@register_series_method
def jenks_bin(s: pd.Series, /, bins: int, **kwargs) -> pd.Series:
    """
    Bin values into discrete intervals via “natural breaks” (Fisher-Jenks algorithm).

    Parameters
    ----------
    bins : int
        The desired number of class. Requires ``2 <= bins < len(s)``.

    **kwargs
        See the documentation for :meth:`pandas.cut` for complete details on
        the keyword arguments.

    Returns
    -------
    Series

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'jenkspy'.

    See Also
    --------
    dtoolkit.accessor.series.bin
    dtoolkit.accessor.series.jenks_breaks

    Notes
    -----
    This method could be called via ``s.jenks_bin`` or ``df.jenks_cut``.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1.3, 7.1, 7.3, 2.3, 3.9, 4.1, 7.8, 1.2, 4.3, 7.3, 5.0, 4.3])
    >>> s
    0     1.3
    1     7.1
    2     7.3
    3     2.3
    4     3.9
    5     4.1
    6     7.8
    7     1.2
    8     4.3
    9     7.3
    10    5.0
    11    4.3
    dtype: float64
    >>> s.jenks_bin(3, include_lowest=True)
    0     (1.199, 2.3]
    1       (5.0, 7.8]
    2       (5.0, 7.8]
    3     (1.199, 2.3]
    4       (2.3, 5.0]
    5       (2.3, 5.0]
    6       (5.0, 7.8]
    7     (1.199, 2.3]
    8       (2.3, 5.0]
    9       (5.0, 7.8]
    10      (2.3, 5.0]
    11      (2.3, 5.0]
    dtype: category
    Categories (3, interval[float64, right]): [(1.199, 2.3] < (2.3, 5.0] < (5.0, 7.8]]
    """

    bins = jenks_breaks(s, bins)
    return pd.cut(s, bins=bins, **kwargs)
