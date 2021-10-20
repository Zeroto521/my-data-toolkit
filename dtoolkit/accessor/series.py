from __future__ import annotations

from textwrap import dedent

import pandas as pd
from pandas.util._decorators import doc
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor._util import get_inf_range
from dtoolkit.accessor.register import register_series_method

__all__ = ["cols", "dropinf", "top_n"]


@register_series_method
@doc(
    returns=dedent(
        """
    Returns
    -------
    str
        The name of the Series.
    """,
    ),
)
def cols(s: pd.Series) -> str:
    """
    A API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    {returns}
    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns

    Examples
    --------
    >>> from dtoolkit.accessor.dataframe import cols
    >>> from dtoolkit.accessor.series import cols
    >>> import pandas as pd

    Get :attr:`~pandas.Series.name`.

    >>> s = pd.Series(range(10), name="item")
    >>> s.cols()
    'item'

    Get :attr:`~pandas.DataFrame.columns`.

    >>> d = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}})
    >>> d.cols()
    ['a', 'b']
    """

    return s.name


@register_series_method
def dropinf(
    s: pd.Series,
    inf: str = "all",
    inplace: bool = False,
) -> pd.Series | None:
    """
    Remove ``inf`` values.

    Parameters
    ----------
    inf : {'all', 'pos', 'neg'}, default 'all'
        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' : Only remove ``inf``.
        * 'neg' : Only remove ``-inf``.

    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    Series or None
        Series with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    dtoolkit.accessor.dataframe.dropinf : :obj:`~pandas.DataFrame` drops rows
        or columns which contain ``inf`` values.

    Examples
    --------
    >>> from dtoolkit.accessor.series import dropinf
    >>> import pandas as pd
    >>> import numpy as np
    >>> ser = pd.Series([1., 2., np.inf])
    >>> ser
    0    1.0
    1    2.0
    2    inf
    dtype: float64

    Drop inf values from a Series.

    >>> ser.dropinf()
    0    1.0
    1    2.0
    dtype: float64

    Keep the Series with valid entries in the same variable.

    >>> ser.dropinf(inplace=True)
    >>> ser
    0    1.0
    1    2.0
    dtype: float64
    """

    inplace = validate_bool_kwarg(inplace, "inplace")
    inf_range = get_inf_range(inf)
    mask = s.isin(inf_range)
    result = s[~mask]

    if not inplace:
        return result

    s._update_inplace(result)


@register_series_method
def bin(
    s: pd.Series,
    bins,
    labels=None,
    right: bool = True,
    retbins: bool = False,
    precision: int = 3,
    include_lowest: bool = False,
    duplicates: str = "raise",
    ordered: bool = False,
    inplace: bool = False,
) -> pd.Series | None:
    """
    Bin values into discrete intervals.

    See Also
    --------
    pandas.cut: This accessor's prototype method.

    Examples
    --------
    >>> from dtoolkit.accessor.series import bin
    >>> import pandas as pd

    Create **score** samples:

    >>> s = pd.Series([100, 10, 50, 20, 90, 60])

    Bin score to rank level:

        - (0, 60] -> E
        - (60, 70] -> D
        - (70, 80] -> C
        - (80, 90] -> B
        - (90, 100] -> A

    >>> s.bin([0, 60, 70, 80, 90, 100], ['E', 'D', 'C', 'B', 'A'], right=True)
    0    A
    1    E
    2    E
    3    E
    4    B
    5    E
    dtype: category
    Categories (5, object): ['E', 'D', 'C', 'B', 'A']
    """
    result = pd.cut(
        s,
        bins=bins,
        right=right,
        labels=labels,
        retbins=retbins,
        precision=precision,
        include_lowest=include_lowest,
        duplicates=duplicates,
        ordered=ordered,
    )

    inplace = validate_bool_kwarg(inplace, "inplace")
    if not inplace:
        return result

    s._update_inplace(result)


@register_series_method
def top_n(
    s: pd.Series,
    n: int,
    largest: bool = True,
    keep: str = "first",
) -> pd.Series:
    """
    Return the top `n` values.

    This method is the collection of
    :meth:`~pandas.Series.nlargest` and :meth:`~pandas.Series.nsmallest`
    methods.

    Except `largest` other parameters is same to
    :meth:`~pandas.Series.nlargest`.

    - If `largest` is True, use :meth:`~pandas.Series.nlargest`
    - If `largest` is False, use :meth:`~pandas.Series.nsmallest`

    See Also
    --------
    pandas.Series.nlargest : Get the largest `n` elements.
    pandas.Series.nsmallest : Get the smallest `n` elements.
    """

    if largest:
        return s.nlargest(n=n, keep=keep)

    return s.nsmallest(n=n, keep=keep)
