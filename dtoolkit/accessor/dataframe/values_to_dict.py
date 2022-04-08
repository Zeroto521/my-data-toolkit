from __future__ import annotations

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import values_to_dict as s_values_to_dict  # noqa


@register_dataframe_method
def values_to_dict(
    df: pd.DataFrame,
    order: list | tuple = None,
    few_as_key: bool = True,
) -> dict:
    """
    Convert :attr:`~pandas.DataFrame.values` to :class:`dict`.

    Parameters
    ----------
    order : list or tuple, optional
        The order of keys via given columns. If ``order`` is set, ``few_as_key``
        will not work.

    few_as_key : bool, default True
        If True the key would be the few unique of column values first.

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
    ...         "z" : [1, 2, 3, 3, 4],
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
    is `x` < `y` < `z`. So the result will be ``{x: {y: [z]} }``.

    >>> print(json.dumps(df.values_to_dict(), indent=4))
    {
        "A": {
            "a": [
                1
            ],
            "b": [
                2
            ]
        },
        "B": {
            "c": [
                3
            ],
            "d": [
                3,
                4
            ]
        }
    }

    Use many unique of column values as key first, the result will be
    ``{y: {z: [x]} }``.

    >>> print(json.dumps(df.values_to_dict(few_as_key=False), indent=4))
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
            1,
            2
        ],
        "B": [
            3,
            3,
            4
        ]
    }
    >>> print(json.dumps(df.values_to_dict(order=["z", "y", "x"]), indent=4))
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

    It also could convert one column DataFrame. But ``few_as_key`` wouldn' work.
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
    """

    if df.shape[1] == 1:  # one columns DataFrame
        return df.to_series().values_to_dict()

    columns = order or (
        df.unique_counts()
        .sort_values(
            ascending=few_as_key,
        )
        .index
    )
    return _dict(df[columns])


def _dict(df: pd.DataFrame) -> dict:
    key_column, *value_column = df.columns

    if df.shape[1] == 2:  # two column DataFrame
        return df.to_series(
            index_column=key_column,
            value_column=value_column[0],
        ).values_to_dict()

    return {
        key: _dict(df.loc[df[key_column] == key, value_column])
        for key in df[key_column].unique()
    }
