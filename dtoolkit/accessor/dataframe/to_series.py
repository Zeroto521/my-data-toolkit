from __future__ import annotations

import pandas as pd

from dtoolkit._typing import IntOrStr
from dtoolkit._typing import SeriesOrFrame
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def to_series(
    df: pd.DataFrame,
    name: IntOrStr = None,
    index_column: IntOrStr = None,
    value_column: IntOrStr = None,
) -> SeriesOrFrame:
    """
    Convert :class:`~pandas.DataFrame` to :class:`~pandas.Series`.

    Parameters
    ----------
    name : str or int, optional
        The name of returned Series.

    index_column : str or int, optional
        The Series's index.

    value_column : str or int, optional
        The Series's value.

    Returns
    -------
    Series or DataFrame

    Raises
    ------
    ValueError
        - If ``index_column`` is same to ``value_column``.
        - If ``index_column`` is not in the columns.
        - If ``value_column`` is not in the columns.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    Convert one column DataFrame to Series.

    >>> df = pd.DataFrame(range(3))
    >>> df
       0
    0  0
    1  1
    2  2
    >>> df.to_series(name="new name")
    0    0
    1    1
    2    2
    Name: new name, dtype: int64

    Can't directly convert two or more columns DataFrame

    >>> df = pd.DataFrame({"a": range(3), "b": range(3, 6), "c": range(6, 9)})
    >>> df
       a  b  c
    0  0  3  6
    1  1  4  7
    2  2  5  8
    >>> df.to_series()
       a  b  c
    0  0  3  6
    1  1  4  7
    2  2  5  8

    Convert to Series with ``index_column`` and ``value_column`` are **both** set.
    A sugar syntax for ``df.set_index(index_column).get(value_column)``.

    >>> df.to_series(index_column="b", value_column="c")
    b
    3    6
    4    7
    5    8
    Name: c, dtype: int64
    """

    if df.columns.__len__() == 1:  # one column DataFrame
        column = df.columns[0]
        return df.get(column).rename(name or column)

    # two and more columns DataFrame
    elif index_column and value_column:
        if index_column == value_column:
            raise ValueError("'index_column' and 'value_column' should be different.")
        elif index_column not in df.columns:
            raise ValueError(f"{index_column!r} is not in the columns.")
        elif value_column not in df.columns:
            raise ValueError(f"{value_column!r} is not in the columns.")

        return (
            df.set_index(index_column)
            .loc[:, value_column]
            .rename(
                name or value_column,
            )
        )

    return df
