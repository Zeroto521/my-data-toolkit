from __future__ import annotations

import pandas as pd

from dtoolkit._typing import IntOrStr
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import values_to_dict as s_values_to_dict  # noqa


@register_dataframe_method
def values_to_dict(
    df: pd.DataFrame,
    order: list[IntOrStr] | pd.Index = None,
    ascending: bool = True,
    unique: bool = True,
    to_list: bool = True,
) -> dict:
    """
    Convert :attr:`~pandas.DataFrame.values` to :class:`dict`.

    Parameters
    ----------
    order : list of str or int, Index, optional
        The order of keys via given columns. If ``order`` is set, ``ascending``
        will not work.

    ascending : bool, default True
        If True the key would use the few unique of column values first.

    unique : bool, default True
        If True would drop duplicate elements.

    to_list : bool, default True
        If True one element value will return :keyword:`list`.

    Returns
    -------
    dict

    See Also
    --------
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

    if len(df.columns) == 1:  # one columns DataFrame
        return df.to_series().values_to_dict(
            unique=unique,
            to_list=to_list,
        )

    columns = order or (
        df.nunique()
        .sort_values(
            ascending=ascending,
        )
        .index
    )

    return df[columns].pipe(
        to_dict,
        unique=unique,
        to_list=to_list,
    )


def to_dict(df: pd.DataFrame, unique: bool, to_list: bool) -> dict:
    key_column, *value_column = df.columns

    if len(df.columns) == 2:  # two column DataFrame
        return df.to_series(
            index_column=key_column,
            value_column=value_column[0],
        ).values_to_dict(
            unique=unique,
            to_list=to_list,
        )

    return {
        key: df.loc[df[key_column] == key, value_column].pipe(
            to_dict,
            unique=unique,
            to_list=to_list,
        )
        for key in df[key_column].unique()
    }
