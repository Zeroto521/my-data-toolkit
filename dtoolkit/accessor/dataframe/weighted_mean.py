from __future__ import annotations

from typing import Hashable

import pandas as pd
from pandas.api.types import is_dict_like
from pandas.api.types import is_number

from dtoolkit._typing import Number
from dtoolkit._typing import SeriesOrFrame
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def weighted_mean(
    df: pd.DataFrame,
    /,
    weights: list[Number] | dict[Hashable, Number | dict[Hashable, Number]] | pd.Series,
    validate: bool = False,
    top: Number = 1,
    drop: bool = False,
) -> SeriesOrFrame:
    """
    Calculate the weighted score of selected columns in the DataFrame.

    The weighted score is the sum of the values in the DataFrame multiplied by
    the weights. A sugar syntax wraps::

        (df * weights).sum(axis=1) / sum(weights)

    Parameters
    ----------
    weights : list, dict or Series
        The weights of each column in the DataFrame.

        - list : The weights of each column in the DataFrame.
        - dict : Receive like ``{column: score}`` or ``{new_column: {column: score}}``.
        - Series : The weights must be a series with the same index as the DataFrame.

    validate : bool, default False
        If True, require the sum of ``weights`` values equal to 1.

    top : int, default 1
        If ``validate`` is True, require the sum of ``weights`` values equal to ``top``.

    drop : bool, default False
        If True, drop the used columns.

    Returns
    -------
    DataFrame or Series

    Raises
    ------
    TypeError
        - If one of the ``weights`` values is not number type.
        - If ``weights`` is not a list, a dict or a Series type.
        - If ``weights`` is a dict and the value is not a number or a dict type.

    ValueError
        - If ``weights`` is list type and its length is not the same as the number of
          DataFrame columns.
        - If ``weights`` is Series type and its labels are not in the DataFrame columns.
        - If ``weights`` is Series type and its labels are duplicated.
        - If ``validate=True`` and the sum of ``weights`` values is not equal to 1.

    See also
    --------
    pandas.DataFrame.mean : Calculate the mean of the DataFrame.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 1], "b": [2, 2], "c": [4, 4]})
    >>> df
       a  b  c
    0  1  2  4
    1  1  2  4

    Select all columns to calculate the score.

    >>> df.weighted_mean([0, 5, 5])
    0    3.0
    1    3.0
    dtype: float64

    Select some of columns and calculate the score.

    >>> df.weighted_mean({'b': 5, 'c': 5})
    0    3.0
    1    3.0
    dtype: float64

    Keep the original columns.

    >>> df.weighted_mean({"bc": {'b': 5, 'c': 5}})
       a  b   bc  c
    0  1  2  3.0  4
    1  1  2  3.0  4

    While ``weights`` is a dict and its values are also dict, it could use new generated
    columns to generate the score.

    >>> df.weighted_mean(
    ...     {
    ...         "ab": {"a": 1, "b": 1},
    ...         "bc": {"b": 1, "c": 1},
    ...         "ab-bc": {"ab": 1, "bc": 1},  # 'ab' and 'bc' are new generated columns
    ...     }
    ... )
       a   ab  ab-bc  b   bc  c
    0  1  1.5   2.25  2  3.0  4
    1  1  1.5   2.25  2  3.0  4
    """

    if isinstance(weights, (list, tuple)):
        result = score(df, weights, validate=validate, top=top)

    elif isinstance(weights, pd.Series):
        result = score(df, weights, validate=validate, top=top, name=weights.name)

    elif isinstance(weights, dict):
        if all(map(is_number, weights.values())):
            result = score(df, weights=weights, validate=validate, top=top)

        elif all(map(is_dict_like, weights.values())):
            result = pd.DataFrame()
            for name, weight in weights.items():
                if not all(map(is_number, weight.values())):
                    raise TypeError("The value of weights is not number type.")

                data = result.combine_first(df)
                another = score(data, weight, validate=validate, top=top, name=name)
                result = pd.concat((result, another), axis=1)

        else:
            raise TypeError("Received an invalid 'weights' type.")

    else:
        raise TypeError(
            "'weights' must be a list, a dict or a Series type, "
            f"but you passed a {type(weights).__name__!r}.",
        )

    if not drop:
        if isinstance(result, pd.Series) and result.name:
            result = result.to_frame()
        if isinstance(result, pd.DataFrame):
            result = result.combine_first(df)

    return result


def score(
    df: pd.DataFrame,
    /,
    weights: list[Number] | dict[Hashable, Number] | pd.Series,
    *,
    validate: bool,
    top: Number,
    name: Hashable = None,
) -> pd.Series:
    """Return calculated single score column."""

    if isinstance(weights, dict):
        df = df[weights.keys()]
        weights = weights.values()
    elif isinstance(weights, pd.Series):
        df = df[weights.index]
        weights = weights.values

    if validate and sum(weights) != top:
        raise ValueError(f"{sum(weights)=} is not equal to {top}.")

    return df.mul(weights).sum(axis=1).divide(sum(weights)).rename(name)
