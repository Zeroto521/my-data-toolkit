from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from pandas.util._validators import validate_bool_kwarg

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.accessor._util import get_mask
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import cols as s_cols
from dtoolkit.accessor.series import expand as s_expand
from dtoolkit.accessor.series import top_n as s_top_n

if TYPE_CHECKING:
    from typing import Iterable


@register_dataframe_method
@doc(
    s_cols,
    returns=dedent(
        """
    Returns
    -------
    list of str or int
        The column names.
    """,
    ),
)
def cols(df: pd.DataFrame) -> list[str | int]:
    return df.columns.tolist()


@register_dataframe_method
def drop_inf(
    df: pd.DataFrame,
    axis: int | str = 0,
    how: str = "any",
    inf: str = "all",
    subset: list[str] | None = None,
    inplace: bool = False,
) -> pd.DataFrame | None:
    """
    Remove ``inf`` values.

    Parameters
    ----------
    axis : {0 or 'index', 1 or 'columns'}, default 0
        Determine if rows or columns which contain ``inf`` values are
        removed.

        * 0, or 'index' : Drop rows which contain ``inf`` values.
        * 1, or 'columns' : Drop columns which contain ``inf`` value.

    how : {'any', 'all'}, default 'any'
        Determine if row or column is removed from :obj:`~pandas.DataFrame`,
        when we have at least one ``inf`` or all ``inf``.

        * 'any' : If any ``inf`` values are present, drop that row or column.
        * 'all' : If all values are ``inf``, drop that row or column.

    inf : {'all', 'pos', 'neg'}, default 'all'
        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' : Only remove ``inf``.
        * 'neg' : Only remove ``-inf``.

    subset : array-like, optional
        Labels along other axis to consider, e.g. if you are dropping rows
        these would be a list of columns to include.
    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    DataFrame or None
        DataFrame with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    dtoolkit.accessor.series.drop_inf
        :obj:`~pandas.Series` drops ``inf`` values.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
    ...                    "toy": [np.inf, 'Batmobile', 'Bullwhip'],
    ...                    "born": [np.inf, pd.Timestamp("1940-04-25"),
    ...                             -np.inf]})
    >>> df
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Drop the rows where at least one element is inf and -inf.

    >>> df.drop_inf()
         name        toy                 born
    1  Batman  Batmobile  1940-04-25 00:00:00

    Drop the columns where at least one element is inf and -inf.

    >>> df.drop_inf(axis='columns')
            name
    0    Alfred
    1    Batman
    2  Catwoman

    Drop the rows where all elements are inf and -inf.

    >>> df.drop_inf(how='all')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Drop the rows where at least one element is -inf.

    >>> df.drop_inf(inf='neg')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00

    Define in which columns to look for inf and -inf values.

    >>> df.drop_inf(subset=['name', 'toy'])
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Keep the DataFrame with valid entries in the same variable.

    >>> df.drop_inf(inplace=True)
    >>> df
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    """
    from dtoolkit.accessor._util import get_inf_range

    inplace = validate_bool_kwarg(inplace, "inplace")

    axis = df._get_axis_number(axis)
    agg_axis = 1 - axis

    agg_obj = df
    if subset is not None:
        ax = df._get_axis(agg_axis)
        indices = ax.get_indexer_for(subset)
        check = indices == -1
        if check.any():
            raise KeyError(list(np.compress(check, subset)))

        agg_obj = df.take(indices, axis=agg_axis)

    inf_range = get_inf_range(inf)
    mask = agg_obj.isin(inf_range)
    mask = get_mask(how, mask, agg_axis)
    result = df.loc(axis=axis)[~mask]

    if not inplace:
        return result

    df._update_inplace(result)


@register_dataframe_method
def filter_in(
    df: pd.DataFrame,
    condition: Iterable | pd.Series | pd.DataFrame | dict[str, list[str]],
    axis: int | str = 0,
    how: str = "all",
    inplace: bool = False,
) -> pd.DataFrame | None:
    """
    Filter :obj:`~pandas.DataFrame` contents.

    Similar to :meth:`~pandas.DataFrame.isin`, but the return is value not
    bool.

    Parameters
    ----------
    condition : iterable, Series, DataFrame or dict
        The result will only be true at a location if all the labels match.

        * If ``condition`` is a :obj:`dict`, the keys must be the row/column
          names, which must match. And ``how`` only works on these gave keys.

            - ``axis`` is 0 or 'index', keys would be recognize as column
              names.
            - ``axis`` is 1 or 'columns', keys would be recognize as index
              names.

        * If ``condition`` is a :obj:`~pandas.Series`, that's the index.

        * If ``condition`` is a :obj:`~pandas.DataFrame`, then both the index
          and column labels must match.

    axis : {0 or 'index', 1 or 'columns'}, default 0
        Determine if rows or columns which contain value are filtered.

        * 0, or 'index' : Filter rows which contain value.
        * 1, or 'columns' : Filter columns which contain value.

    how : {'any', 'all'}, default 'all'
        Determine if row or column is filtered from :obj:`~pandas.DataFrame`,
        when we have at least one value or all value.

        * 'any' : If any values are present, filter that row or column.
        * 'all' : If all values are present, filter that row or column.

    inplace : bool, default is False
        If True, do operation inplace and return None.

    Returns
    -------
    DataFrame

    See Also
    --------
    pandas.DataFrame.isin
        Whether each element in the DataFrame is contained in values.
    pandas.DataFrame.filter
        Subset the dataframe rows or columns according to the specified index
        labels.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({'num_legs': [2, 4, 2], 'num_wings': [2, 0, 0]},
    ...                   index=['falcon', 'dog', 'cat'])
    >>> df
            num_legs  num_wings
    falcon         2          2
    dog            4          0
    cat            2          0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> df.filter_in([0, 2])
            num_legs  num_wings
    falcon         2          2
    cat            2          0

    Filter columns.

    >>> df.filter_in([0, 2], axis=1)
                num_wings
    falcon          2
    dog             0
    cat             0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    row/column (depend on ``axis``) separately.

    Filter rows, to check under the column (key) whether contains the value.

    >>> df.filter_in({'num_legs': [2], 'num_wings': [2]})
            num_legs  num_wings
    falcon         2          2

    Filter columns, to check under the index (key) whether contains the value.

    >>> df.filter_in({'cat': [2]}, axis=1)
            num_legs
    falcon         2
    dog            4
    cat            2

    When ``values`` is a Series or DataFrame the index and column must match.
    Note that 'spider' doesn't match based on the number of legs in ``other``.

    >>> other = pd.DataFrame({'num_legs': [8, 2], 'num_wings': [0, 2]},
    ...                      index=['spider', 'falcon'])
    >>> other
            num_legs  num_wings
    spider         8          0
    falcon         2          2
    >>> df.filter_in(other)
            num_legs  num_wings
    falcon         2          2
    """
    from dtoolkit.accessor._util import isin

    inplace = validate_bool_kwarg(inplace, "inplace")
    axis = df._get_axis_number(axis)

    another_axis = 1 - axis

    mask = isin(df, condition, axis)
    if isinstance(condition, dict):
        # 'how' only works on condition's keys
        names = condition.keys()
        mask = mask[names] if axis == 0 else mask.loc[names]
    mask = get_mask(how, mask, another_axis)

    result = df.loc(axis=axis)[mask]
    if not inplace:
        return result

    df._update_inplace(result)


@register_dataframe_method
def repeat(
    df: pd.DataFrame,
    repeats: int | list[int],
    axis: int | str = 0,
) -> pd.DataFrame | None:
    """
    Repeat row or column of a :obj:`~pandas.DataFrame`.

    Returns a new DataFrame where each row/column is repeated
    consecutively a given number of times.

    Parameters
    ----------
    repeats : int or array of ints
        The number of repetitions for each element. This should be a
        non-negative integer. Repeating 0 times will return an empty
        :obj:`~pandas.DataFrame`.

    axis : {0 or 'index', 1 or 'columns'}, default 0
        The axis along which to repeat.

        * 0, or 'index' : Along the row to repeat.
        * 1, or 'columns' : Along the column to repeat.

    Returns
    -------
    DataFrame
        Newly created DataFrame with repeated elements.

    See Also
    --------
    numpy.repeat : This transformer's prototype method.

    Examples
    --------
    >>> import pandas as pd
    >>> import dtoolkit.accessor
    >>> df = pd.DataFrame({'a': [1, 2], 'b':[3, 4]})
    >>> df
       a  b
    0  1  3
    1  2  4

    Each row repeat two times.

    >>> df.repeat(2)
       a  b
    0  1  3
    0  1  3
    1  2  4
    1  2  4

    Each column repeat two times.

    >>> df.repeat(2, 1)
       a  a  b  b
    0  1  1  3  3
    1  2  2  4  4

    ``a`` column repeat 1 times, ``b`` column repeat 2 times.

    >>> df.repeat([1, 2], 1)
       a  b  b
    0  1  3  3
    1  2  4  4
    """

    axis = df._get_axis_number(axis)
    return pd.DataFrame(
        np.repeat(
            df._values,
            repeats,
            axis=axis,
        ),
        index=df.index.repeat(repeats) if axis == 0 else df.index,
        columns=df.columns.repeat(repeats) if axis == 1 else df.columns,
    )


@register_dataframe_method
def top_n(
    df: pd.DataFrame,
    n: int,
    largest: bool = True,
    keep: str = "first",
    prefix: str = "top",
    delimiter: str = "_",
    element: str = "index",
) -> pd.DataFrame:
    """
    Returns each row's top `n`.

    Parameters
    ----------
    n : int
        Number of top to return.

    largest : bool, default True
        - True, the top is the largest.
        - False, the top is the smallest.

    keep : {"first", "last", "all"}, default "first"
        Where there are duplicate values:

        - first : prioritize the first occurrence(s).
        - last : prioritize the last occurrence(s).
        - all : do not drop any duplicates, even it means selecting more than
          n items.

    prefix : str, default "top"
        The prefix name of the new DataFrame column.

    delimiter : str, default "_"
        The delimiter between `prefix` and number.

    element : {"both", "index", "value"}, default "index"
        To control the structure of return dataframe value.

        - both: the structure of value is ``({column index}, {value})``.
        - index: the structure of value is only ``{column index}``.
        - value: the structure of value is only ``{value}``.

    Returns
    -------
    DataFrame
        - The structure of column name is ``{prefix}{delimiter}{number}``.
        - The default structure of value is ``{column index}`` and could be
          controled via ``element``.

    See Also
    --------
    dtoolkit.accessor.dataframe.expand
        Transform each element of a list-like to a column.

    Notes
    -----
    Q: Any different to :meth:`~pandas.DataFrame.nlargest` and
    :meth:`~pandas.DataFrame.nsmallest`?

    A: :meth:`~pandas.DataFrame.nlargest` and
    :meth:`~pandas.DataFrame.nsmallest` base one column to return all selected
    columns dataframe top `n`.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "a": [1, 3, 2, 1],
    ...         "b": [3, 2, 1, 1],
    ...         "c": [2, 1, 3, 1],
    ...     },
    ... )
    >>> df
       a  b  c
    0  1  3  2
    1  3  2  1
    2  2  1  3
    3  1  1  1

    Get each row's largest top **2**.

    >>> df.top_n(2)
        top_1   top_2
    0       b       c
    1       a       b
    2       c       a
    3       a       b

    Get each row's both **index** and **value** of largest top 2.

    >>> df.top_n(2, element="both")
        top_1   top_2
    0  (b, 3)  (c, 2)
    1  (a, 3)  (b, 2)
    2  (c, 3)  (a, 2)
    3  (a, 1)  (b, 1)

    Get each row's smallest top **1** and **keep** the duplicated values.

    >>> df.top_n(1, largest=False, keep="all")
        top_1   top_2   top_3
    0       a     NaN     NaN
    1       c     NaN     NaN
    2       b     NaN     NaN
    3       a       b       c
    """

    if element not in ("both", "index", "value"):
        raise ValueError('element must be either "both", "index" or "value"')

    def wrap_s_top_n(*args, **kwargs) -> pd.Series:
        top = s_top_n(*args, **kwargs)

        if element == "both":
            data = zip(top.index, top.values)
        elif element == "index":
            data = top.index
        elif element == "value":
            data = top.values

        return pd.Series(data, index=pd.RangeIndex(1, len(top) + 1))

    return df.apply(
        wrap_s_top_n,
        axis=1,
        n=n,
        largest=largest,
        keep=keep,
    ).add_prefix(prefix + delimiter)


@register_dataframe_method
@doc(
    s_expand,
    see_also=dedent(
        """
    See Also
    --------
    dtoolkit.accessor.series.expand
        Transform each element of a list-like to a column.
    pandas.DataFrame.explode
        Transform each element of a list-like to a row.
    """,
    ),
    examples=dedent(
        """
    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> import numpy as np

    Expand the *list-like* element.

    >>> df = pd.DataFrame({'A': [[0, 1, 2], 'foo', [], [3, 4]],
    ...                    'B': 1,
    ...                    'C': [['a', 'b', 'c'], np.nan, [], ['d', 'e']]})
    >>> df.expand()
        A_0  A_1  A_2  B   C_0   C_1   C_2
    0     0  1.0  2.0  1     a     b     c
    1   foo  NaN  NaN  1   NaN  None  None
    2  None  NaN  NaN  1  None  None  None
    3     3  4.0  NaN  1     d     e  None

    Expand *sub-element* type is list-like.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [("a", "b"), (3, (5, 6))]})
    >>> df.expand(flatten=True)
       col1 col2_0 col2_1  col2_2
    0     1      a      b     NaN
    1     2      3      5     6.0

    Set the columns of name.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [("a", 3), ("b", 4)]})
    >>> df.expand(suffix=["index", "value"], delimiter="-")
       col1  col2-index  col2-value
    0     1           a           3
    1     2           b           4

    Also could handle **different lengths** of element and suffix list.

    >>> df = pd.DataFrame({"col1": [1, 2], "col2": [(3, 4), (5, 6, 7)]})
    >>> df.expand()
       col1  col2_0  col2_1  col2_2
    0     1       3       4     NaN
    1     2       5       6     7.0
    >>> df.expand(suffix=["a", "b", "c", "d"])
       col1  col2_a  col2_b  col2_c
    0     1       3       4     NaN
    1     2       5       6     7.0
    """,
    ),
)
def expand(
    df: pd.DataFrame,
    suffix: list[str | int] | None = None,
    delimiter: str = "_",
    flatten: bool = False,
) -> pd.DataFrame:
    return pd.concat(
        (
            df.get(key=column).expand(
                suffix=suffix,
                delimiter=delimiter,
                flatten=flatten,
            )
            for column in df.cols()
        ),
        axis=1,
    )


@register_dataframe_method
def to_series(df: pd.DataFrame, name: str | int = None) -> SeriesOrFrame:
    """
    Transform one column :class:`~pandas.DataFrame` to :class:`~pandas.Series`.

    Parameters
    ----------
    name : str or int, optional
        The name of returned Series

    Returns
    -------
    Series or DataFrame
        Series if ``df`` is one column else would be DataFrame.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(range(3))
    >>> df
       0
    0  0
    1  1
    2  2
    >>> df.to_series()
    0    0
    1    1
    2    2
    Name: 0, dtype: int64
    >>> df = pd.DataFrame({'a': [1, 2]})
    >>> df
       a
    0  1
    1  2
    >>> df.to_series()
    0    1
    1    2
    Name: a, dtype: int64
    """

    if df.shape[1] == 1:  # one column DataFrame
        column = df.columns[0]
        return df.get(column).rename(name or column)

    return df
