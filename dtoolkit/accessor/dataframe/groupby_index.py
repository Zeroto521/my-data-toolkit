import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def groupby_index(df: pd.DataFrame, /, **kwargs) -> pd.core.groupby.DataFrameGroupBy:
    """
    Group DataFrame by its index.

    Parameters
    ----------
    **kwargs
        See the documentation for :meth:`~pandas.DataFrame.groupby` for complete
        details on the keyword arguments except ``by``.

    Returns
    -------
    DataFrameGroupBy

    See Also
    --------
    pandas.DataFrame.groupby
    dtoolkit.accessor.series.groupby_index

    Notes
    -----
    ``by`` parameter is set to ``df.index`` and can't be overridden.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({'a': [1, 1, 1], 'b': [1, 2, 3]}, index=['a', 'b', 'a'])
    >>> df
       a  b
    a  1  1
    b  1  2
    a  1  3
    >>> df.groupby_index().sum()
       a  b
    a  2  4
    b  1  2
    """

    return df.groupby(df.index, **kwargs)
