import pandas as pd

from dtoolkit.accessor.register import register_series_method
from dtoolkit.geoaccessor.index import is_h3 as i_is_h3


@register_series_method
def is_h3(s: pd.Series, /) -> bool:
    """
    Validate whether the whole Series is H3 cell index.

    Returns
    -------
    bool
        True if the whole Series is H3 cell index else False.

    See Also
    --------
    dtoolkit.geoaccessor.index.is_h3
    dtoolkit.geoaccessor.series.H3.is_valid

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Series(string) or Series(int64) dtype.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    String type H3 cell index.

    >>> s = pd.Series(['a', 'b'], index=['88143541bdfffff', '886528b2a3fffff'])
    >>> s
    88143541bdfffff    a
    886528b2a3fffff    b
    dtype: object
    >>> s.is_h3()
    True

    Int type H3 cell index.

    >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
    >>> s
    612845052823076863    a
    614269156845420543    b
    dtype: object
    >>> s.is_h3()
    True
    """

    return i_is_h3(s.index)
