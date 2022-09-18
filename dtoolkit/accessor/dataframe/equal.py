from warnings import catch_warnings
from warnings import simplefilter
from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_array_like

from dtoolkit._typing import Axis
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.util._exception import find_stack_level


@register_dataframe_method
def equal(
    df: pd.DataFrame,
    /,
    other,
    align: bool = True,
    axis: Axis = 0,
    **kwargs,
) -> pd.DataFrame:
    """
    Return a boolean DataFrame containing the result of comparing with ``other``.

    A sugar syntax for ``np.equal(df, other, **kwargs)``.

    Parameters
    ----------
    other : scalar, 1d array-like or 2d array-like
        The value(s) to compare with the DataFrame.
        - scalar : compare each element with the scalar value.
        - 1d / 2d array-like : compare each element with the corresponding value.

    align : bool, default True
        If True, align ``df`` and ``other`` before comparing.
        Only works wihle ``other`` is a Series / DataFrame.

    axis : {0 or 'index', 1 or 'columns'}, default 0
        If 0, compare along ``df``'s rows else columns. Works only when ``other`` is
        1d array-like.

    **kwargs
        Additional keyword arguments are passed to :meth:`numpy.equal`.

    Returns
    -------
    DataFrame

    Warns
    -----
    UserWarning
        If ``align`` is True and ``other`` is a Series / DataFrame, but its
        indexes (columns) are not equal to ``df``.

    Raises
    ------
    ValueError
        If ``other`` is id array-like and its size is not equal to ``df``'s size.

    See Also
    --------
    pandas.DataFrame.eq : Compare two Series.
    numpy.equal : Return (x1 == x2) element-wise.
    dtoolkit.accessor.series.equal : Series version of ``.equal``.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
    >>> df
       a  b
    0  1  3
    1  2  2
    2  3  1

    Like ``DataFrame.eq`` method to compare scalar or array-like via ``==``,
    ``DataFrame.equal`` could also do that.

    Compare with a scalar.

    >>> df == 1
           a      b
    0   True  False
    1  False  False
    2  False   True
    >>> df.equal(1)
           a      b
    0   True  False
    1  False  False
    2  False   True

    Compare with a 1d array-like.

    But ``==`` only can compare along the row. ``DataFrame.equal`` can compare along
    the row or column.

    >>> df == [1, 2]
           a      b
    0   True  False
    1  False   True
    2  False  False
    >>> df.equal([1, 2], axis=0)  # default compare along the row
           a      b
    0   True  False
    1  False   True
    2  False  False
    >>> df.equal([1, 2, 3], axis=0)  # default compare along the column
    """

    axis = df._get_axis_number(axis)
    if align and (
        isinstance(other, pd.Series)
        and not df.index.equals(other.index)
        or isinstance(other, pd.DataFrame)
        and not df.index.equals(other.index)
        and not df.columns.equals(other.columns)
    ):
        warn("the indices are different.", stacklevel=find_stack_level())
        df, other = df.align(
            other,
            axis=1 - axis if isinstance(other, pd.Series) else None,
        )

    if is_array_like(other):
        other = np.asarray(other)
        if other.ndim == 1 and other.size != df.shape[1 - axis]:
            raise ValueError(
                f"size of other ({other.shape[0]}) does not equal to df.shape"
                f"[{1-axis}] ({df.shape[1 - axis]})."
            )

        if other.ndim == 1 and axis == 1:
            other = other.reshape((-1, 1))

    with catch_warnings():
        # TODO: remove `catch_warnings` in the future.
        # The latest pandas version (1.4.x) doesn't specify a version when
        # it will change the behavior on non-aligned DataFrame.

        # Original message:
        # FutureWarning: Calling a ufunc on non-aligned DataFrames(or DataFrame/Series
        # combination). Currently, the indices are ignored and the result takes the
        # index/columns of the first DataFrame. In the future , the DataFrames/Series
        # will be aligned before applying the ufunc. Convert one of the arguments to a
        # NumPy array (eg 'ufunc(df1, np.asarray(df2)') to keep the current behaviour,
        # or align manually (eg 'df1, df2 = df1.align(df2)') before passing to the ufunc
        # to obtain the future behaviour and silence this warning.
        simplefilter("ignore", FutureWarning)
        return np.equal(df, other, **kwargs)
