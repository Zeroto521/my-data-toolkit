from functools import partial

import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_index_method


@register_index_method
@doc(klass="Index")
def is_h3(index: pd.Index, /) -> bool:
    """
    Validate whether the {klass} is H3 cell index.

    Returns
    -------
    bool
        True if the {klass} is H3 cell index else False.

    See Also
    --------
    dtoolkit.geoaccessor.index.is_h3
    dtoolkit.geoaccessor.series.is_h3
    dtoolkit.geoaccessor.dataframe.is_h3
    dtoolkit.geoaccessor.index.H3.is_valid
    dtoolkit.geoaccessor.series.H3.is_valid
    dtoolkit.geoaccessor.dataframe.H3.is_valid

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If the Index dtype is not string or int64.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd

    String type H3 cell index.

    >>> index = pd.Index(['88143541bdfffff', '886528b2a3fffff'])
    >>> index
    Index(['88143541bdfffff', '886528b2a3fffff'], dtype='str')
    >>> index.is_h3()
    True
    >>> s = pd.Series(['a', 'b'], index=['88143541bdfffff', '886528b2a3fffff'])
    >>> s
    88143541bdfffff    a
    886528b2a3fffff    b
    dtype: str
    >>> s.is_h3()
    True
    >>> df = pd.DataFrame(
    ...     {{'label': ['a', 'b']}},
    ...     index=['88143541bdfffff', '886528b2a3fffff'],
    ... )
    >>> df
                    label
    88143541bdfffff     a
    886528b2a3fffff     b
    >>> df.is_h3()
    True

    Int type H3 cell index.

    >>> index = pd.Index([612845052823076863, 614269156845420543])
    >>> index
    Index([612845052823076863, 614269156845420543], dtype='int64')
    >>> index.is_h3()
    True
    >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
    >>> s
    612845052823076863    a
    614269156845420543    b
    dtype: str
    >>> s.is_h3()
    True
    >>> df = pd.DataFrame(
    ...     {{'label': ['a', 'b']}},
    ...     index=[612845052823076863, 614269156845420543],
    ... )
    >>> df
                       label
    612845052823076863     a
    614269156845420543     b
    >>> df.is_h3()
    True
    """

    return all(apply_h3(index, "is_valid_cell"))


def apply_h3(index: pd.Index, /, method: str, **kwargs) -> list:
    """
    Apply H3 method to :obj:`~pandas.Index`.

    Parameters
    ----------
    method : str
        H3 method name.

    **kwargs
        Additional keyword arguments are passed to ``h3.{method}``.

    Returns
    -------
    list

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If not Index(string) or Index(int64) dtype.
    """

    if is_integer_dtype(index):
        # NOTE: Can't use `__import__("h3.api.numpy_int")`
        # See https://github.com/uber/h3-py/issues/304
        import h3.api.numpy_int as h3
    elif is_string_dtype(index):
        import h3.api.basic_str as h3
    else:
        raise TypeError(
            f"Expected Index(string) or Index(int64), but got {index.dtype!r}",
        )

    func = partial(getattr(h3, method), **kwargs)
    return list(map(func, index))
