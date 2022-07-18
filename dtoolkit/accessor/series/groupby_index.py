import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def groupby_index(s: pd.Series, /, **kwargs) -> pd.core.groupby.SeriesGroupBy:
    """
    Group Series by its index.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~pandas.Series.groupby` for complete
        details on the keyword arguments except ``by``.

    Returns
    -------
    SeriesGroupBy

    See Also
    --------
    pandas.Series.groupby
    dtoolkit.accessor.dataframe.groupby_index

    Notes
    -----
    ``by`` parameter is set to ``s.index`` and can't be overridden.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1, 1, 1], index=['a', 'b', 'a'])
    >>> s
    a    1
    b    1
    a    1
    dtype: int64
    >>> s.groupby_index().count()
    a    2
    b    1
    dtype: int64
    """

    return s.groupby(s.index, **kwargs)
