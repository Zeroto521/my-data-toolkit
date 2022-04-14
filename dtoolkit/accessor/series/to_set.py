import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_set(s: pd.Series):
    """
    Return a :keyword:`set` of the values.

    A sugary syntax wraps :keyword:`set`::
        set(s)

    See Also
    --------
    pandas.Series.unique

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 2])
    >>> s.to_set()
    {1, 2}

    Different to :meth:`pandas.Series.unique`.

    >>> s.unique()
    array([1, 2], dtype=int64)
    """

    return set(s)
