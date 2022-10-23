import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def to_datetime(s: pd.Series, /, **kwargs) -> pd.Series:
    """
    Convert Series to datetime type.

    A sugary syntax wraps::

        pd.to_datetime(s, **kwargs)

    Parameters
    ----------
    **kwargs
        Keyword arguments to pass to :meth:`pandas.to_datetime`.

    Returns
    -------
    Series

    See Also
    --------
    pandas.to_datetime

    Notes
    -----
    ``DataFrame.to_datetime`` could use `janitor.functions.to_datetime`__.

    __ https://pyjanitor-devs.github.io/pyjanitor/api/functions/\
#janitor.functions.to_datetime

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(['20200101', '20200202', '20200303'])
    >>> s
    0    20200101
    1    20200202
    2    20200303
    dtype: object
    >>> s.to_datetime(format='%Y%m%d')
    0   2020-01-01
    1   2020-02-02
    2   2020-03-03
    dtype: datetime64[ns]
    """

    return pd.to_datetime(s, **kwargs)
