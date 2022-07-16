from __future__ import annotations

from textwrap import dedent
from typing import Hashable
from typing import Iterable

import pandas as pd
from pandas.api.types import is_list_like
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_series_method


@register_series_method
@doc(
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
    /,
    suffix: list[Hashable] = None,
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
    suffix : list of Hashable, optional
        New columns of return :class:`~pandas.DataFrame`.

    delimiter : str, default "_"
        The delimiter between :attr:`~pandas.Series.name` and `suffix`.

    flatten : bool, default False
        Flatten all like-list elements or not. It would cost more time.

    Returns
    -------
    DataFrame
        The structure of new column name is ``{{column name}}{{delimiter}}{{suffix}}``.

    Raises
    ------
    ValueError
        - If ``s.name`` is None.
        - If ``len(suffix)`` less than the max size of ``s``'s elements.

    See Also
    --------
    pandas.Series.explode
        Transform each element of a list-like to a row.

    pandas.DataFrame.explode
        Transform each element of a list-like to a row.

    dtoolkit.accessor.series.expand
        Transform each element of a list-like to a column.

    dtoolkit.accessor.dataframe.expand
        Transform each element of a list-like to a column.
    {examples}
    """

    s_list = s.apply(_wrap_collapse, flatten=flatten)
    s_len = s_list.len()
    if all(s_len == 1):
        return s

    if s.name is None:
        raise ValueError("the column name should be specified.")

    max_len = s_len.max()
    if suffix and len(suffix) < max_len:
        raise ValueError(
            f"suffix length is less than the max size of {s.name!r} elements.",
        )

    columns = suffix or range(max_len)
    return pd.DataFrame(
        s_list.tolist(),
        index=s.index,
        columns=columns[:max_len],
    ).add_prefix(s.name + delimiter)


def _wrap_collapse(x, flatten: bool) -> list:
    if is_list_like(x):
        return list(collapse(x)) if flatten else x
    return [x]


# based on more_itertools/more.py
def collapse(iterable: Iterable):
    def walk(node):
        if isinstance(node, (str, bytes)):
            yield node
            return

        try:
            tree = iter(node)
        except TypeError:
            yield node
            return
        else:
            for child in tree:
                yield from walk(child)

    yield from walk(iterable)
