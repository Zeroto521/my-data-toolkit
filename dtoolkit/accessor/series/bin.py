import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method("cut")
@register_series_method
def bin(s: pd.Series, /, *args, **kwargs) -> pd.Series:
    """
    Bin values into discrete intervals.

    A sugary syntax wraps :meth:`~pandas.cut`::

        pd.cut(s, *args, **kwargs)

    Parameters
    ----------
    *args, **kwargs
        See the documentation for :meth:`pandas.cut` for complete details on
        the positional arguments and the keyword arguments.

    Returns
    -------
    Series

    See Also
    --------
    pandas.cut
    dtoolkit.accessor.series.jenks_bin

    Notes
    -----
    This method could be called via ``s.bin`` or ``s.cut``.

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

    return pd.cut(s, *args, **kwargs)
