import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def invert_or_not(s: pd.Series, /, invert: bool = False) -> pd.Series:
    """
    Invert (~) the Series.

    Parameters
    ----------
    invert : bool, default is False
        If True, invert the Series.

    Returns
    -------
    Series(bool)

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series([True, False, True])
    >>> s
    0     True
    1    False
    2     True
    dtype: bool
    >>> s.invert_or_not()
    0     True
    1    False
    2     True
    dtype: bool
    >>> s.invert_or_not(invert=True)
    0    False
    1     True
    2    False
    dtype: bool
    """

    return ~s if invert else s
