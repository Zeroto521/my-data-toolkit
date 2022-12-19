from typing import Callable

import pandas as pd
from pandas.api.types import is_int64_dtype
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method
from dtoolkit.geoaccessor.index.is_h3 import method_from_h3


@register_series_method
def is_h3(s: pd.Series, /) -> bool:
    """
    Validate whether the whole series is H3 cell index.

    Returns
    -------
    bool
        True if the whole series is H3 cell index else False.

    See Also
    --------
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

    >>> s = pd.Series(['88143541bdfffff', '886528b2a3fffff'])
    >>> s
    0    88143541bdfffff
    1    886528b2a3fffff
    dtype: object
    >>> s.is_h3()
    True

    Int type H3 cell index.

    >>> s = pd.Series([612845052823076863, 614269156845420543])
    >>> s
    0    612845052823076863
    1    614269156845420543
    dtype: int64
    >>> s.is_h3()
    True
    """

    # TODO: Use `is_valid_cell` instead of `h3_is_valid`
    # While h3-py release 4, `is_valid_cell` is not available.
    return s.apply(method_from_h3(s, "h3_is_valid")).all()
