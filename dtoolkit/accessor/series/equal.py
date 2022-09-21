from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._exception import find_stack_level


@register_series_method
def equal(s: pd.Series, /, other, align: bool = True, **kwargs) -> pd.Series:
    """
    Return a boolean Series containing the result of comparing with ``other``.

    A sugar syntax for ``np.equal(s, other, **kwargs)``.

    Parameters
    ----------
    other : scalar or 1d array-like
        The value(s) to compare with the Series.

        - scalar : compare each element with the scalar value.
        - 1d array-like : compare each element with the corresponding value.

    align : bool, default True
        If True, align ``s`` and ``other`` before comparing. Only works while
        ``other`` is a Series.

    **kwargs
        Additional keyword arguments are passed to :meth:`numpy.equal`.

    Returns
    -------
    Series

    Warns
    -----
    UserWarning
        If ``align`` is True and ``other`` is a Series, but its indexes are not
        equal to ``s``.

    Raises
    ------
    ValueError
        If the lengths of ``s`` and ``other`` are not equal.

    See Also
    --------
    pandas.Series.eq : Compare two Series.
    numpy.equal : Return (x1 == x2) element-wise.
    dtoolkit.accessor.dataframe.equal : DataFrame version of ``.equal``.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 3])
    >>> s
    0    1
    1    2
    2    3
    dtype: int64

    Like ``Series.eq`` method to compare scalar or array-like via ``==``,
    ``Series.equal`` could also do that.

    Compare with scalar.

    >>> s == 2
    0    False
    1     True
    2    False
    dtype: bool
    >>> s.equal(2)
    0    False
    1     True
    2    False
    dtype: bool

    Compare with array-like.

    >>> s.equal(pd.Series([3, 2, 1]))
    0    False
    1     True
    2    False
    dtype: bool
    >>> s.equal(pd.Series([3, 2, 1]))
    0    False
    1     True
    2    False
    dtype: bool

    ``s.equal`` can also compare with array-like based on index.

    >>> s == pd.Series([3, 2, 1], index=[2, 1, 0])  # doctest: +SKIP
    ValueError: Can only compare identically-labeled Series objects
    >>> s.equal(pd.Series([3, 2, 1], index=[2, 1, 0]))
    0    True
    1    True
    2    True
    dtype: bool
    >>> s.equal(pd.Series([3, 2, 1], index=[2, 1, 0]), align=False)
    0    False
    1     True
    2    False
    dtype: bool
    """

    if align and isinstance(other, pd.Series) and not s.index.equals(other.index):
        warn("the indices are different.", stacklevel=find_stack_level())
        s, other = s.align(other)

    if is_list_like(other):
        other = np.asarray(other)

    return np.equal(s, other, **kwargs)
