import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.to_set import to_set


@register_series_method
def duplicated_groups(s: pd.Series) -> pd.Series:
    """
    Labels of duplicate elements.

    Returns
    -------
    Series

    See Also
    --------
    pandas.Series.duplicated
    pandas.Series.value_counts

    Example
    -------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(["b", "b", "a", "b"])
    >>> s
    0    b
    1    b
    2    a
    3    b
    dtype: object
    >>> s.duplicated_groups()
    0    0
    1    0
    2    1
    3    0
    dtype: int64
    """

    base_elements = to_set(s)
    return s.replace(dict(zip(base_elements, range(len(base_elements)))))
