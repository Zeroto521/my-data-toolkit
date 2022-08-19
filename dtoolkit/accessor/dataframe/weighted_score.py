from typing import Hashable

import pandas as pd

from dtoolkit.accessor.index import to_set
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit._typing import Number


@register_dataframe_method("weighted_average")
@register_dataframe_method("weighted_mean")
@register_dataframe_method
def weighted_score(
    df: pd.DataFrame,
    /,
    weights: list[Number] | dict[Hashable, Number | dict[Hashable, Number]] | pd.Series,
    drop: bool = False,
) -> pd.DataFrame | pd.Series:
    """
    Calculate the weighted score of selected columns in the DataFrame.

    The weighted score is the sum of the values in the DataFrame multiplied by the weights.

    Parameters
    ----------
    weights : list, dict or Series
        The weights of each column in the DataFrame.
        - list : The weights of each column in the DataFrame.
        - dict :
        - Series : The weights must be a series with the same index as the DataFrame.

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
        - weights is list type
            - If the length of weights is not the same as the number of DataFrame
             columns.

        - weights is Series type
            - If the labels of the weights are not in the DataFrame columns.
            - If the labels of the weights are duplicated.

    Notes
    -----
    This method could be called via ``df.weighted_score``, ``df.weighted_mean``,
    or ``df.weighted_average``.
    """

    if isinstance(weights, (list, tuple, pd.Series)):
        name = weights.name if isinstance(weights, pd.Series) else None
        return score(df, weights=weights, name=name)
    elif isinstance(weights, dict):
        ...

    raise TypeError(
        f"weights ({type(weights).__name__!r}) must be list, dict or Series type."
    )


def score(
    df: pd.DataFrame,
    /,
    weights: list[Number] | pd.Series,
    name: Hashable = None,
) -> pd.Series:
    if isinstance(weights, pd.Series) and (
        not to_set(weights.index) <= to_set(df.columns)
    ):
        raise ValueError(
            f"One of the weights ({weights!r}) is not in the DataFrame columns "
            f"({to_set(df.columns)!r})."
        )

    return ((df * weights).sum(axis=1) / sum(weights)).rename(name)
