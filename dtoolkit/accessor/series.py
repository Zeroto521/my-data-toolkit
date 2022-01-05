from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pandas as pd
from pandas.util._decorators import doc
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor.register import register_series_method

if TYPE_CHECKING:
    from typing import Any

    from dtoolkit._typing import OneDimArray


@register_series_method
@doc(
    returns=dedent(
        """
    Returns
    -------
    str or None
        The name of the Series.
    """,
    ),
)
def cols(s: pd.Series) -> str | None:
    """
    An API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    {returns}
    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns
    dtoolkit.accessor.series.cols
    dtoolkit.accessor.dataframe.cols

    Examples
    --------
    >>> import dtoolkit.accessor
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
def drop_inf(
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
    dtoolkit.accessor.dataframe.drop_inf
        :obj:`~pandas.DataFrame` drops rows or columns which contain ``inf``
        values.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> import numpy as np
    >>> s = pd.Series([1., 2., np.inf])
    >>> s
    0    1.0
    1    2.0
    2    inf
    dtype: float64

    Drop inf values from a Series.

    >>> s.drop_inf()
    0    1.0
    1    2.0
    dtype: float64

    Keep the Series with valid entries in the same variable.

    >>> s.drop_inf(inplace=True)
    >>> s
    0    1.0
    1    2.0
    dtype: float64
    """
    from dtoolkit.accessor._util import get_inf_range

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
    >>> import dtoolkit.accessor
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
    inplace = validate_bool_kwarg(inplace, "inplace")

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

    Parameters
    ----------
    n : int
        Number of top to return.

    largest : bool, default True
        - True, the top is the largest.
        - True, the top is the smallest.

    keep : {"first", "last", "all"}, default "first"
        Where there are duplicate values:

        - first : prioritize the first occurrence(s).
        - last : prioritize the last occurrence(s).
        - all : do not drop any duplicates, even it means selecting more than
          n items.

    Returns
    -------
    Series

    See Also
    --------
    dtoolkit.accessor.series.expand
        Transform each element of a list-like to a column.
    dtoolkit.accessor.dataframe.top_n
        Returns each row's top n.
    """

    if largest:
        return s.nlargest(n=n, keep=keep)

    return s.nsmallest(n=n, keep=keep)


@register_series_method
@doc(
    see_also=dedent(
        """
    See Also
    --------
    pandas.Series.explode
        Transform each element of a list-like to a row.
    dtoolkit.accessor.dataframe.expand
        Transform each element of a list-like to a column.
    """,
    ),
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    Expand the *list-like* element.

    >>> s = pd.Series([[1, 2, 3], 'foo', [], [3, 4]], name="item")
    >>> s.expand()
       item_0  item_1  item_2
    0       1     2.0     3.0
    1     foo     NaN     NaN
    2    None     NaN     NaN
    3       3     4.0     NaN

    Expand *sub-element* type is list-like.

    >>> s = pd.Series([("a", "b"), [1, [2, 3]]], name="item")
    >>> s.expand(flatten=True)
       item_0  item_1  item_2
    0       a       b     NaN
    1       1       2     3.0

    Set the columns of name.

    >>> s = pd.Series([("a", 1), ["b", 2]], name="item")
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
    """,
    ),
)
def expand(
    s: pd.Series,
    suffix: list[str | int] | None = None,
    delimiter: str = "_",
    flatten: bool = False,
) -> pd.DataFrame:
    """
    Transform each element of a list-like to a **column**.

    .. image:: ../../../../_static/expand-vs-explode.svg
        :width: 80%
        :align: center

    Parameters
    ----------
    suffix : list of str or int, default None
        New columns of return :class:`~pandas.DataFrame`.

    delimiter : str, default "_"
        The delimiter between :attr:`~pandas.Series.name` and `suffix`.

    flatten : bool, default False
        Flatten all like-list elements or not. It would cost more time.

    Returns
    -------
    DataFrame
        The structure of new column name is ``{{column name}}{{delimiter}}{{suffix}}``.
    {see_also}
    {examples}
    """
    from pandas.api.types import is_list_like

    from dtoolkit.accessor._util import collapse

    def wrap_collapse(x) -> list[Any]:
        if is_list_like(x):
            if flatten:
                return list(collapse(x))
            return x
        return [x]

    s_list = s.apply(wrap_collapse)
    s_len = s_list.lens()
    if all(s_len == 1):
        return s

    max_len = s_len.max()
    if suffix and len(suffix) < max_len:
        raise ValueError(
            f"suffix length is less than the max size of {s.name!r} elements.",
        )

    if s.name is None:
        raise ValueError("the column name should be specified.")

    columns = suffix or range(max_len)
    return pd.DataFrame(
        s_list.tolist(),
        index=s.index,
        columns=columns[:max_len],
    ).add_prefix(s.name + delimiter)


@register_series_method
def lens(s: pd.Series) -> pd.Series:
    """
    Return the length of each element in the series.

    Equals to::

        s.apply(len)

    Returns
    -------
    Series

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([0, 1, "string", ("tuple",), ["list"], {}, object])
    >>> s
    0                   0
    1                   1
    2              string
    3            (tuple,)
    4              [list]
    5                  {}
    6    <class 'object'>
    dtype: object
    >>> s.lens()
    0    1.0
    1    1.0
    2    6.0
    3    1.0
    4    1.0
    5    0.0
    6    NaN
    dtype: float64
    """
    from pandas.api.types import is_number

    def wrap_len(x) -> int | None:
        if hasattr(x, "__len__"):
            return len(x)
        elif is_number(x):
            return 1

    return s.apply(wrap_len)


@register_series_method
def error_report(
    s: pd.Series,
    predicted: OneDimArray | list[int | float],
    columns: list[str | int] | None = None,
) -> pd.DataFrame:
    """
    Calculate `absolute error` and `relative error` of two columns.

    Parameters
    ----------
    predicted : list of int or float, ndarrray, Series
        A array is compared to ``s``.
    columns : list of str or int, default None
        The columns of returning DataFrame, each represents `true value`,
        `predicted value`, `absolute error`, and `relative error`.

    Returns
    -------
    DataFrame
        Return four columns DataFrame and each represents `true value`,
        `predicted value`, `absolute error`, and `relative error`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 3])
    >>> s.error_report([3, 2, 1])
       true value  predicted value  absolute error  relative error
    0           1                3               2        2.000000
    1           2                2               0        0.000000
    2           3                1               2        0.666667

    If the name of ``s`` or ``predicted`` is not None, the columns of
    ``error_report`` would use the name of ``s`` and ``predicted``.

    >>> s = pd.Series([1, 2, 3], name="y")
    >>> predicted = pd.Series([3, 2, 1], name="y predicted")
    >>> s.error_report(predicted)
       y  y predicted  absolute error  relative error
    0  1            3               2        2.000000
    1  2            2               0        0.000000
    2  3            1               2        0.666667

    If ``columns`` is not None, the columns of ``error_report`` would use it
    firstly.

    >>> s.error_report(predicted, columns=["a", "b", "c", "d"])
       a  b  c         d
    0  1  3  2  2.000000
    1  2  2  0  0.000000
    2  3  1  2  0.666667
    """

    if len(s) != len(predicted):
        raise IndexError(
            "Length of 'predicted' doesn't match length of 'reference'.",
        )

    if isinstance(predicted, pd.Series):
        if not s.index.equals(predicted.index):
            raise IndexError(
                "Index values of 'predicted' sequence doesn't "
                "match index values of 'reference'.",
            )
    else:
        predicted = pd.Series(predicted, index=s.index)

    if columns is None:
        columns = [
            s.name or "true value",
            predicted.name or "predicted value",
            "absolute error",
            "relative error",
        ]
    elif len(columns) != 4:
        raise IndexError("The length of 'columns' is not equal to 4.")

    absolute_error = (predicted - s).abs()
    relative_error = absolute_error / s

    return pd.concat(
        [
            s,
            predicted,
            absolute_error,
            relative_error,
        ],
        axis=1,
        keys=columns,
    )


@register_series_method
def get_attr(s: pd.Series, name: str, *args, **kwargs) -> pd.Series:
    """
    Return the value of the named attribute of Series element.

    The back core logical is :func:`getattr`.

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

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])

    Get a attribute.

    >>> s.get_attr("__doc__")
    0    str(object='') -> str\\nstr(bytes_or_buffer[, e...
    1    str(object='') -> str\\nstr(bytes_or_buffer[, e...
    dtype: object

    Get a don't exist attribute.

    >>> s.get_attr("whatever")
    0    None
    1    None
    dtype: object

    Get a method attribute and call it.

    >>> s.get_attr("count", "l")
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
