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
    drop: bool = False,
) -> pd.DataFrame | pd.Series:
    """
    Calculate the weighted score of selected columns in the DataFrame.

    The weighted score is the sum of the values in the DataFrame multiplied by
    the weights.

    Parameters
    ----------
    weights : list, dict or Series
        The weights of each column in the DataFrame.
        - list : The weights of each column in the DataFrame.
        - dict : Receive datastructure like ``{column: score}`` or
         ``{new_column: {column: score}}``.
        - Series : The weights must be a series with the same index as the DataFrame.

    drop : bool, default False
        If True, drop the used columns.

    validate : bool, default False
        If True, require the sum of weights values equal to 1.

    Returns
    -------
    DataFrame or Series

    Raises
    ------
    TypeError
        - If one of the weight values is not number type.
        - If weights is not a list, a dict or a Series type.

    ValueError
        - weights is list type
            - If the length of weights is not the same as the number of DataFrame
             columns.

        - weights is Series type
            - If the labels of the weights are not in the DataFrame columns.
            - If the labels of the weights are duplicated.
    """

    # HACK: Figure out how to handle the relationship between `weights`` (array-like)
    # and `drop`.
    # the result of array-like type `weights` is a Series (or single column DataFrame).
    # It don't have a 'name'. So how to combine with the original DataFrame?

    if isinstance(weights, list, tuple):
        return score(df, weights=weights)

    if isinstance(weights, pd.Series):
        if to_set(weights.index) > to_set(df.columns):
            raise ValueError(
                f"One of the 'weights' elements ({to_set(weights.index)!r}) is not in "
                f"the DataFrame columns ({to_set(df.columns)!r}).",
            )

        return score(df, weights=weights, name=weights.name)

    elif isinstance(weights, dict):
        ...
    else:
        raise TypeError(
            "'weights' must be a list, a dict or a Series type, "
            f"but you passed a {type(weights).__name__!r}.",
        )


def score(
    df: pd.DataFrame,
    /,
    weights: list[Number] | pd.Series,
    name: Hashable = None,
    validate: bool = False,
) -> pd.Series:
    """Return calculated single score column."""

    sum_weights = sum(weights)
    if validate and sum_weights != 1:
        raise ValueError(
            f"The sum of weights values ({sum_weights!r}) is not equal to 1."
        )

    return ((df * weights).sum(axis=1) / sum_weights).rename(name)
