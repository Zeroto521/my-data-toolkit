import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_set(s: pd.Series, /) -> set:
    """
    Return a :keyword:`set` of the values.

    A sugary syntax wraps :keyword:`set`::

        set(s)

    Returns
    -------
    set

    See Also
    --------
    pandas.Series.unique
    dtoolkit.accessor.index.to_set

    Notes
    -----
    Different to :meth:`~pandas.Index.unique`, it returns :class:`~pandas.Index`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 2])
    >>> s
    0    1
    1    2
    2    2
    dtype: int64
    >>> s.to_set()
    {1, 2}
    """

    return set(s.to_list())
