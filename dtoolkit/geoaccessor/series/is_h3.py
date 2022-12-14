import pandas as pd

from pandas.api.types import is_string_dtype
from pandas.api.types import is_int64_dtype

from dtoolkit.accessor.register import register_series_method


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
    h3.h3_is_valid

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    Str type H3 cell index.

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

    # requires h3 >= 4
    # from h3.api.numpy_int import is_valid_cell
    # requires h3 < 4
    if is_int64_dtype(s):
        is_valid = __import__("h3").api.numpy_int.h3_is_valid
    elif is_string_dtype(s):
        is_valid = __import__("h3").api.basic_str.h3_is_valid
    else:
        raise TypeError(
            f"Expected Series(string) or Series(int64), but got {s.dtype!r}"
        )

    return s.apply(is_valid).all()
