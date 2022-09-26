from __future__ import annotations

from typing import Hashable

import pandas as pd

from dtoolkit._typing import Number
from dtoolkit.accessor.index import to_set
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def weighted_mean(
    df: pd.DataFrame,
    /,
    weights: list[Number] | dict[Hashable, Number | dict[Hashable, Number]] | pd.Series,
    validate: bool = False,
    drop: bool = False,
) -> pd.DataFrame | pd.Series:
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
        - dict : Receive datastructure like ``{column: score}`` or
         ``{new_column: {column: score}}``.
        - Series : The weights must be a series with the same index as the DataFrame.

    validate : bool, default False
        If True, require the sum of ``weights`` values equal to 1.

    drop : bool, default False
        If True, drop the used columns.

    Returns
    -------
    DataFrame or Series

    Raises
    ------
    TypeError
        - If one of the weight values is not number type.
        - If weights is not a list, a dict or a Series type.

    ValueError
        - If ``weights`` is list type and its length is not the same as the number of
          DataFrame columns.
        - If ``weights`` is Series type and its labels are not in the DataFrame columns.
        - If ``weights`` is Series type and its labels are duplicated.
        - If ``validate=True`` and the sum of ``weights`` values is not equal to 1.
    """

    # HACK: Figure out how to handle the relationship between `weights`` (array-like)
    # and `drop`.
    # the result of array-like type `weights` is a Series (or single column DataFrame).
    # It don't have a 'name'. So how to combine with the original DataFrame?

    if isinstance(weights, list, tuple):
        result = score(df, weights=weights, validate=validate)
    elif isinstance(weights, pd.Series):
        if to_set(weights.index) > to_set(df.columns):
            raise ValueError(
                f"One of the 'weights' elements ({to_set(weights.index)!r}) is not in "
                f"the DataFrame columns ({to_set(df.columns)!r}).",
            )

        result = score(df, weights=weights, validate=validate, name=weights.name)
    elif isinstance(weights, dict):
        ...
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
    weights: list[Number] | pd.Series,
    name: Hashable = None,
    validate: bool = False,
) -> pd.Series:
    """Return calculated single score column."""

    sum_w = sum(weights)
    if validate and sum_w != 1:
        raise ValueError(f"The sum of weights values ({sum_w!r}) is not equal to 1.")

    return ((df * weights).sum(axis=1) / sum_w).rename(name)
