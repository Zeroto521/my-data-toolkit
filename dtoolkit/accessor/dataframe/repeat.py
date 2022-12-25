from __future__ import annotations

from typing import Hashable

import pandas as pd
from pandas.api.types import is_number

from dtoolkit._typing import Axis
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def repeat(
    df: pd.DataFrame,
    repeats: int | Hashable | list[int],
    /,
    axis: Axis = 0,
) -> pd.DataFrame:
    """
    Repeat row or column of a :obj:`~pandas.DataFrame`.

    Returns a new DataFrame where each row/column is repeated
    consecutively a given number of times.

    A sugary syntax wraps :meth:`numpy.repeat`.

    Parameters
    ----------
    repeats : int, Hashable or array of ints
        The number of repetitions for each element. This should be a non-negative
        integer. Repeating 0 times will return an empty :obj:`~pandas.DataFrame`.
        The order of priority type is ``int`` > ``Hashable``.

        * int : the row or column will be repeated ``repeats`` times.

        * array of int : the row or column at the i-th position will be repeated.
          Its length must be the same as the axis being repeated.

        * Hahsable : the row or column will be repeated by with the given column.

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
    >>> import dtoolkit
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

    Use the 'a' column to repeat the row.

    >>> df.repeat('a')
       a  b
    0  1  3
    1  2  4
    1  2  4
    """

    if not is_number(repeats) and isinstance(repeats, Hashable):
        repeats = df[repeats]

    return df.reindex(df._get_axis(axis).repeat(repeats), axis=axis)
