import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def swap_index_values(s: pd.Series, /) -> pd.Series:
    """
    Swap the index and values of the Series.

    A sugary syntax wraps::

        pd.Series(s.index, index=s)

    Returns
    -------
    Series

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     [1, 2, 3],
    ...     index=pd.Index(
    ...         ["a", "b", "c"],
    ...         name='index',
    ...     ),
    ...     name='values',
    ... )
    >>> s
    index
    a    1
    b    2
    c    3
    Name: values, dtype: int64
    >>> s.swap_index_values()
    values
    1    a
    2    b
    3    c
    Name: index, dtype: object
    """

    return pd.Series(s.index, index=s)
