from __future__ import annotations

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method(name="getattr")
@register_series_method
def get_attr(s: pd.Series, name: str, *args, **kwargs) -> pd.Series:
    """
    Return the value of the named attribute of Series element.

    The back core logical is :func:`getattr`.

    Read more in the `User Guide`_.

    .. _User Guide: ../../guide/tips_about_getattr.ipynb

    Parameters
    ----------
    name : str
        The name of one of the Series element's attributes. If the named attribute
        does not exist, None is returned.
    args, kwargs
        The arguments of the function type attribute.

    Returns
    -------
    Series

    See Also
    --------
    getattr

    Notes
    -----
    To keep the Python naming style, so use this accessor via
    ``Series.getattr`` rather than ``Series.get_attr``.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])

    Get a attribute.

    >>> s.getattr("__doc__")
    0    str(object='') -> str\\nstr(bytes_or_buffer[, e...
    1    str(object='') -> str\\nstr(bytes_or_buffer[, e...
    dtype: object

    Get a don't exist attribute.

    >>> s.getattr("whatever")
    0    None
    1    None
    dtype: object

    Get a method attribute and call it.

    >>> s.getattr("count", "l")
    0    2
    1    1
    dtype: int64
    """

    def wrap_getattr(x):
        attr = getattr(x, name, None)
        if callable(attr):
            return attr(*args, **kwargs)
        return attr

    return s.apply(wrap_getattr)
