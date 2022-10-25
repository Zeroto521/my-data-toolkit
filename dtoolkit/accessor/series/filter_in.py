from typing import Iterable

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def filter_in(
    s: pd.Series,
    condition: Iterable,
    /,
    complement: bool = False,
) -> pd.Series:
    """
    Filter :obj:`~pandas.Series` contents.

    Similar to :meth:`~pandas.Series.isin`, but the return is not bool.

    Parameters
    ----------
    condition : list-like
        The filtered result is based on this specific condition.

    complement : bool, default is False
        If True, do operation reversely.

    Returns
    -------
    Series

    See Also
    --------
    pandas.Series.isin
    pandas.Series.filter
    dtoolkit.accessor.dataframe.filter_in
        Filter DataFrame contents.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     ['lama', 'cow', 'lama', 'beetle', 'lama', 'hippo'],
    ...     name='animal',
    ... )
    >>> s
    0      lama
    1       cow
    2      lama
    3    beetle
    4      lama
    5     hippo
    Name: animal, dtype: object
    >>> s.filter_in(['cow', 'lama'])
    0      lama
    1       cow
    2      lama
    4      lama
    Name: animal, dtype: object
    >>> s.filter_in(['cow', 'lama'], complement=True)
    3    beetle
    5     hippo
    Name: animal, dtype: object
    """

    return s[invert_or_not(s.isin(condition), invert=complement)]


def invert_or_not(s: pd.Series, /, invert: bool = False) -> pd.Series:
    """
    Invert (~) the Series.

    Parameters
    ----------
    invert : bool, default is False
        If True, invert the Series.

    Returns
    -------
    Series

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([True, False, True])
    >>> s
    0     True
    1    False
    2     True
    dtype: bool
    >>> s.pipe(invert_or_not)
    0     True
    1    False
    2     True
    dtype: bool
    >>> s.pipe(invert_or_not, invert=True)
    0    False
    1     True
    2    False
    dtype: bool
    """

    return ~s if invert else s
