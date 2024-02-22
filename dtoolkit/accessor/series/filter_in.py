from typing import Iterable

import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.invert_or_not import invert_or_not


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
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series(
    ...     ['llama', 'cow', 'llama', 'beetle', 'llama', 'hippo'],
    ...     name='animal',
    ... )
    >>> s
    0      llama
    1       cow
    2      llama
    3    beetle
    4      llama
    5     hippo
    Name: animal, dtype: object
    >>> s.filter_in(['cow', 'llama'])
    0      llama
    1       cow
    2      llama
    4      llama
    Name: animal, dtype: object
    >>> s.filter_in(['cow', 'llama'], complement=True)
    3    beetle
    5     hippo
    Name: animal, dtype: object
    """

    return s[invert_or_not(s.isin(condition), invert=complement)]
