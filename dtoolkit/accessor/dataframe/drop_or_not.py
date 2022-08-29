import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def drop_or_not(df: pd.DataFrame, /, drop: bool = True, **kwargs) -> pd.DataFrame:
    """
    Drop specified labels from rows or columns.

    A sugary syntax wraps :meth:`~pandas.DataFrame.drop`::

        df.drop(**kwargs) if drop else df

    Parameters
    ----------
    drop : bool, default True
        Choose to drop or not. If True will drop else don't.

    **kwargs
        See the documentation for :meth:`~pandas.DataFrame.drop` for complete
        details on the keyword arguments.

    Returns
    -------
    DataFrame
        If ``drop=True`` will execute else return the original.

    See Also
    --------
    pandas.DataFrame.drop

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> df
       a  b
    0  1  3
    1  2  4
    >>> df.drop_or_not(True, columns="b")
       a
    0  1
    1  2
    >>> df.drop_or_not(False, columns=["a"])
       a  b
    0  1  3
    1  2  4
    """

    return df.drop(**kwargs) if drop else df
