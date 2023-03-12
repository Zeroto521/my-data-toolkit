from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def drop_not_duplicates(
    s: pd.Series,
    /,
    keep: Literal["first", "last", False] = False,
) -> pd.Series:
    """
    Return duplicate Series values.

    A sugary syntax wraps :meth:`~pandas.Series.duplicated`::

        s[s.duplicated(keep=keep)]

    Parameters
    ----------
    keep : {'first', 'last', False}, default ``False``
        Method to handle duplicates:
        - 'first' : Keep duplicates except for the first occurrence.
        - 'last' : Keep duplicates except for the last occurrence.
        - ``False`` : Keep all duplicates.

    Returns
    -------
    Series
        Kept duplicate values.

    See Also
    --------
    pandas.Series.duplicated
    pandas.Series.drop_duplicates
    dtoolkit.accessor.dataframe.drop_not_duplicates

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> animals = pd.Series(['lama', 'cow', 'lama', 'beetle', 'lama'])
    >>> animals
    0      lama
    1       cow
    2      lama
    3    beetle
    4      lama
    dtype: object
    >>> animals.drop_not_duplicates()
    0      lama
    2      lama
    4      lama
    dtype: object
    """

    return s[s.duplicated(keep=keep)]
