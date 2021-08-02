from __future__ import annotations

import pandas as pd
from numpy import inf
from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from ._typing import Pd

__all__ = [
    "ColumnAccessor",
    "DropInfAccessor",
    "FilterInAccessor",
]


class Accessor:
    def __init__(self, pd_obj: Pd):
        self.pd_obj = pd_obj


@register_dataframe_accessor("cols")
@register_series_accessor("cols")
class ColumnAccessor(Accessor):
    """
    A API to gather `pandas.Series.name` and `pandas.DataFrame.columns`
    to one.

    Return the column labels of the DataFrame if it is `DataFrame`.
    Return the name of the Series if it is `Series`.

    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns
    """

    def __call__(self) -> str | list[str]:
        if isinstance(self.pd_obj, pd.Series):
            return self.pd_obj.name

        return self.pd_obj.columns.tolist()


@register_dataframe_accessor("dropinf")
@register_series_accessor("dropinf")
class DropInfAccessor(Accessor):
    def __call__(self, inplace: bool = False) -> Pd | None:
        mask = ~self.pd_obj.isin([inf, -inf])
        if isinstance(self.pd_obj, pd.DataFrame):
            mask = mask.all(axis=1)

        result = self.pd_obj[mask]

        if inplace:
            self.pd_obj._update_inplace(result)
            return None

        return result


@register_dataframe_accessor("filterin")
class FilterInAccessor(Accessor):
    def __call__(
        self,
        cond: dict[str, list[str]],
        inplace: bool = False,
    ) -> pd.DataFrame | None:
        mask_all = self.pd_obj.isin(cond)
        mask_selected = mask_all[cond.keys()]
        result = self.pd_obj[mask_selected.all(axis=1)]

        if inplace:
            self.pd_obj._update_inplace(result)
            return None

        return result


@register_dataframe_accessor("repeat")
class RepeatAccessor(Accessor):
    """
    Repeat row or column of a DataFrame.

    Returns a new DataFrame where each row/column
    is repeated consecutively a given number of times.

    Parameters
    ----------
    repeats : int or array of ints
        The number of repetitions for each element. This should be a
        non-negative integer. Repeating 0 times will return an empty
        DataFrame.
    axis : int
        The axis along which to repeat. By default, along **row** to repeat.

    Returns
    -------
    DataFrame
        Newly created DataFrame with repeated elements.

    See Also
    --------
    numpy.repeat : Similar method for :class:`numpy.ndarray`.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.accessor import RepeatAccessor
    >>> df = pd.DataFrame({'a': [1, 2], 'b':[3, 4]})
    >>> df
       a  b
    0  1  3
    1  2  4

    Each row repeat two times

    >>> df.repeat(2)
       a  b
    0  1  3
    0  1  3
    1  2  4
    1  2  4

    Each column repeat two times

    >>> df.repeat(2, 1)
       a  a  b  b
    0  1  1  3  3
    1  2  2  4  4

    'a' column repeat 1 times, 'b' column repeat 2 times

    >>> df.repeat([1, 2], 1)
       a  b  b
    0  1  3  3
    1  2  4  4
    """

    def __call__(
        self,
        repeats: int | list[int],
        axis: int = 0,
    ) -> pd.DataFrame | None:
        if axis == 0:
            new_index = self.pd_obj.index.repeat(repeats)
            new_column = self.pd_obj.columns.copy()
        elif axis == 1:
            new_index = self.pd_obj.index.copy()
            new_column = self.pd_obj.columns.repeat(repeats)
        else:
            msg = "axis must be 0 (row) or 1 (column), default is 0."
            raise ValueError(msg)

        new_values = self.pd_obj._values.repeat(repeats, axis)
        return pd.DataFrame(
            new_values,
            index=new_index,
            columns=new_column,
        )
