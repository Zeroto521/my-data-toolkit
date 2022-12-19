from __future__ import annotations

from typing import Callable

import pandas as pd
from pandas.api.types import is_int64_dtype
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_index_method


@register_index_method
def is_h3(index: pd.Index, /) -> bool:
    """
    Validate whether the whole :obj:`~pandas.Index` is H3 cell index.

    Returns
    -------
    bool
        True if the whole Index is H3 cell index else False.

    See Also
    --------
    dtoolkit.geoaccessor.index.H3.is_valid

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Index(string) or Index(int64) dtype.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    String type H3 cell index.

    >>> index = pd.Index(['88143541bdfffff', '886528b2a3fffff'])
    >>> index
    Index(['88143541bdfffff', '886528b2a3fffff'], dtype='object')
    >>> index.is_h3()
    True

    Int type H3 cell index.

    >>> index = pd.Index([612845052823076863, 614269156845420543])
    Int64Index([612845052823076863, 614269156845420543], dtype='int64')
    >>> index.is_h3()
    True
    """

    # TODO: Use `is_valid_cell` instead of `h3_is_valid`
    # While h3-py release 4, `is_valid_cell` is not available.
    return index.map(method_from_h3(index, "h3_is_valid")).all()


def method_from_h3(data: pd.Index | pd.Series, method: str, /) -> Callable:
    """
    Based on the Series dtype to get the corresponding H3 method.

    Parameters
    ----------
    data : :obj:`~pandas.Index` or :obj:`~pandas.Series`
        The data to be validated.

    method : str
        H3 method name.

    Returns
    -------
    Callable
        H3 method.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Series(string) or Series(int64) dtype.
    """

    if is_int64_dtype(data):
        # NOTE: Can't use `__import__("h3.api.numpy_int")`
        # See https://github.com/uber/h3-py/issues/304
        import h3.api.numpy_int as h3
    elif is_string_dtype(data):
        import h3.api.basic_str as h3
    else:
        raise TypeError(
            f"Expected Index(string) or Index(int64), but got {data.dtype!r}",
        )

    return getattr(h3, method)
