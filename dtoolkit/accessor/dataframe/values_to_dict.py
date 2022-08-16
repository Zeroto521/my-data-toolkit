from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit.accessor.dataframe.to_series import to_series
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import values_to_dict as s_values_to_dict


@register_dataframe_method
def values_to_dict(
    df: pd.DataFrame,
    /,
    order: list[Hashable] | pd.Index = None,
    ascending: bool = True,
    unique: bool = True,
    to_list: bool = True,
    dropna: bool = True,
) -> dict:
    """
    Convert :attr:`~pandas.DataFrame.values` to :class:`dict`.

    Parameters
    ----------
    order : list of Hashable, Index, optional
        The order of keys via given columns. If ``order`` is set, ``ascending``
        will not work.

    ascending : bool, default True
        If True the key would use the few unique of column values first.

    unique : bool, default True
        If True would drop duplicate elements.

    to_list : bool, default True
        If True one element value will return :class:`list`.

    dropna : bool, default True
        If True it will drop the ``nan`` value whatever it's key or value.

    Returns
    -------
    dict

    Raises
    ------
    ValueError
        If the columns of the inputting is not unique.

    See Also
    --------
    pandas.DataFrame.to_dict
    dtoolkit.accessor.series.values_to_dict

    Notes
    -----
    The same key of values would be merged into :class:`list`.

    Examples
    --------
    >>> import json
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "x" : ["A", "A", "B", "B", "B"],
    ...         "y" : ["a", "b", "c", "d", "d"],
    ...         "z" : ["1", "2", "3", "3", "4"],
    ...     }
    ... )
    >>> df
       x  y  z
    0  A  a  1
    1  A  b  2
    2  B  c  3
    3  B  d  3
    4  B  d  4

    Use few unique of column values as key first. The order of column unique values
    number is `x` < `y` < `z`. So the result will be ``{x: {y: [z]} }``.

    >>> print(json.dumps(df.values_to_dict(), indent=4))
    {
        "A": {
            "a": [
                "1"
            ],
            "b": [
                "2"
            ]
        },
        "B": {
            "c": [
                "3"
            ],
            "d": [
                "3",
                "4"
            ]
        }
    }

    Use many unique of column values as key first, the result will be
    ``{y: {z: [x]} }``.

    >>> print(json.dumps(df.values_to_dict(ascending=False), indent=4))
    {
        "a": {
            "1": [
                "A"
            ]
        },
        "b": {
            "2": [
                "A"
            ]
        },
        "c": {
            "3": [
                "B"
            ]
        },
        "d": {
            "3": [
                "B"
            ],
            "4": [
                "B"
            ]
        }
    }

    Output the arbitrary order like ``{z: x}  or ``{x: {z: [y]} }``,
    via ``order`` argument.

    >>> print(json.dumps(df.values_to_dict(order=["x", "z"]), indent=4))
    {
        "A": [
            "1",
            "2"
        ],
        "B": [
            "3",
            "4"
        ]
    }
    >>> print(json.dumps(df.values_to_dict(order=["x", "z", "y"]), indent=4))
    {
        "A": {
            "1": [
                "a"
            ],
            "2": [
                "b"
            ]
        },
        "B": {
            "3": [
                "c",
                "d"
            ],
            "4": [
                "d"
            ]
        }
    }

    It also could convert one column DataFrame. But ``ascending`` wouldn' work.
    The result would be ``{index: [values]}``.

    >>> print(json.dumps(df[["x"]].values_to_dict(), indent=4))
    {
        "0": [
            "A"
        ],
        "1": [
            "A"
        ],
        "2": [
            "B"
        ],
        "3": [
            "B"
        ],
        "4": [
            "B"
        ]
    }

    Unpack one element value list.

    >>> print(json.dumps(df.values_to_dict(to_list=False), indent=4))
    {
        "A": {
            "a": "1",
            "b": "2"
        },
        "B": {
            "c": "3",
            "d": [
                "3",
                "4"
            ]
        }
    }
    """

    if not df.columns.is_unique:
        raise ValueError("The columns of the inputting is not unique.")

    columns = order or df.nunique().sort_values(ascending=ascending).index
    return to_dict(
        dropna_or_not(df[columns], drop=dropna),
        unique=unique,
        to_list=to_list,
        dropna=dropna,
    )


def dropna_or_not(df: pd.DataFrame, drop: bool, **kwargs) -> pd.DataFrame:
    """Dropna or not."""

    return df.dropna(**kwargs) if drop else df


def to_dict(df: pd.DataFrame, unique: bool, to_list: bool, dropna: bool) -> dict:
    """Iterate over columns pairwise to generate :class:`dic`."""

    if df.columns.size == 0 or df.empty:  # empty DataFrame
        return {}

    elif df.columns.size == 1:  # one columns DataFrame
        return s_values_to_dict(
            to_series(df),
            unique=unique,
            to_list=to_list,
            dropna=dropna,
        )

    elif df.columns.size == 2:  # two columns DataFrame
        key_column, value_column = df.columns

        return to_series(
            df,
            index_column=key_column,
            value_column=value_column,
        ).values_to_dict(
            unique=unique,
            to_list=to_list,
            dropna=dropna,
        )

    # three or more columns DataFrame
    key_column, *value_column = df.columns
    return {
        key: to_dict(
            df.loc[df[key_column] == key, value_column],
            unique=unique,
            to_list=to_list,
            dropna=dropna,
        )
        for key in df[key_column].unique()
    }
