from typing import Iterable

import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.invert_or_not import invert_or_not  # noqa: F401


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

    return s[s.isin(condition).invert_or_not(invert=complement)]
