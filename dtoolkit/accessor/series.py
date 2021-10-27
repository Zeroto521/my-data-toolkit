from __future__ import annotations

from textwrap import dedent

import pandas as pd
from pandas.api.types import is_list_like
from pandas.util._decorators import doc
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor._util import get_inf_range
from dtoolkit.accessor.register import register_series_method


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
    >>> s = pd.Series([1., 2., np.inf])
    >>> s
    0    1.0
    1    2.0
    2    inf
    dtype: float64

    Drop inf values from a Series.

    >>> s.dropinf()
    0    1.0
    1    2.0
    dtype: float64

    Keep the Series with valid entries in the same variable.

    >>> s.dropinf(inplace=True)
    >>> s
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


@register_series_method
def expand(
    s: pd.Series,
    suffix: list | None = None,
    delimiter: str = "_",
) -> pd.DataFrame:
    """
    Transform each element of a list-like to a **column**.

    .. image:: ../../../../_static/expand-vs-explode.svg
        :width: 80%
        :align: center

    Parameters
    ----------
    suffix : list of str, default None
        New columns of return :class:`~pandas.DataFrame`.

    delimiter : str, default "_"
        The delimiter between :attr:`~pandas.Series.name` and `suffix`.

    Returns
    -------
    DataFrame
        The structure of new column name is ``{column name}{delimiter}{suffix}``.

    See Also
    --------
    pandas.Series.explode : Transform each element of a list-like to a row.
    pandas.DataFrame.expand : Transform each element of a list-like to a column.

    Examples
    --------
    >>> from dtoolkit.accessor.series import expand
    >>> import pandas as pd

    Expand the *list-like* element.

    >>> s = pd.Series([("a", 1), ["b", 2]], name="item")
    >>> s.expand()
       item_0  item_1
    0       a       1
    1       b       2

    Set the columns of name.

    >>> s.expand(suffix=["index", "value"], delimiter="-")
       item-index  item-value
    0           a           1
    1           b           2

    Also could handle **different lengths** of element and suffix list.

    >>> s = pd.Series([(1, 2), [1, 2, 3]], name="item")
    >>> s.expand()
       item_0  item_1  item_2
    0       1       2     NaN
    1       1       2     3.0
    >>> s.expand(suffix=["a", "b", "c", "d"])
       item_a  item_b  item_c
    0       1       2     NaN
    1       1       2     3.0
    """

    if not is_list_like(s):
        return s

    if not s.apply(is_list_like).all():
        raise ValueError("all elements should be list-like.")

    if s.name is None:
        raise ValueError("the column name should be specified.")

    max_len = s.apply(len).max()
    if suffix and len(suffix) < max_len:
        raise ValueError(
            f"suffix length is less than the max size of {s.name!r} elements.",
        )

    iters = suffix or range(max_len)
    columns = (s.name + delimiter + str(i) for i in iters[:max_len])

    return pd.DataFrame(s.tolist(), columns=columns)
