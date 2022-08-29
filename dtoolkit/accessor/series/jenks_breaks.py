from __future__ import annotations

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def jenks_breaks(s: pd.Series, /, bins: int) -> list[float]:
    """
    Compute “natural breaks” (Fisher-Jenks algorithm) on Series.

    Parameters
    ----------
    bins : int
        The desired number of class. Requires ``2 <= bins < len(s)``.

    Returns
    -------
    list of floats

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'jenkspy'.

    See Also
    --------
    jenkspy.jenks_breaks
        https://github.com/mthh/jenkspy

    dtoolkit.accessor.series.bin
    dtoolkit.accessor.series.jenks_bin

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
    >>> s.jenks_breaks(3)
    [1.2, 2.3, 5.0, 7.8]
    """
    from jenkspy import jenks_breaks

    return jenks_breaks(s, bins)
