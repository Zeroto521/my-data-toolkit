from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from pandas.util._validators import validate_bool_kwarg

from ..util import multi_if_else
from .base import Accessor
from .series import _get_inf_range


class DataFrameAccessor(Accessor):
    def _validate_inplace(self, inplace: bool) -> bool:
        return validate_bool_kwarg(inplace, "inplace")

    def _validate_axis(self, axis: int | str) -> int:
        if isinstance(axis, (tuple, list)):
            msg = "supplying multiple axes to axis is no longer supported."
            raise TypeError(msg)

        return self.pd_obj._get_axis_number(axis)

    def isin(
        self,
        values: Iterable | pd.Serie | pd.DataFrame | dict[str, list[str]],
        axis: int = 0,
    ) -> pd.DataFrame:
        """
        Extend :meth:`~pandas.DataFrame.isin` function. When ``values`` is
        :obj:`dict` and ``axis`` is 1, ``values``' key could be index name.
        """

        if isinstance(values, dict) and axis == 1:
            values = defaultdict(list, values)
            return pd.concat(
                (
                    self.pd_obj.iloc[[i], :].isin(values[ind])
                    for i, ind in enumerate(self.pd_obj.index)
                ),
                axis=0,
            )

        return self.pd_obj.isin(values)


@register_dataframe_accessor("dropinf")
class DropInfDataFrameAccessor(DataFrameAccessor):
    """
    Remove ``inf`` values.

    Parameters
    ----------
    axis : {0 or 'index', 1 or 'columns'}, default 0
        Determine if rows or columns which contain ``inf`` values are
        removed.

        * 0, or 'index' : Drop rows which contain ``inf`` values.
        * 1, or 'columns' : Drop columns which contain ``inf`` value.

    how : {'any', 'all'}, default 'any'
        Determine if row or column is removed from :obj:`~pandas.DataFrame`,
        when we have at least one ``inf`` or all ``inf``.

        * 'any' : If any ``inf`` values are present, drop that row or column.
        * 'all' : If all values are ``inf``, drop that row or column.

    inf : {'all', 'pos', 'neg'}, default 'all'
        * 'all' : Remove :obj:`numpy.inf`: and -:obj:`numpy.inf`.
        * 'pos' : Only remove :obj:`numpy.inf`:.
        * 'neg' : Only remove -:obj:`numpy.inf`:.

    subset : array-like, optional
        Labels along other axis to consider, e.g. if you are dropping rows
        these would be a list of columns to include.
    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    DataFrame or None
        DataFrame with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    DropInfSeriesAccessor : :obj:`~pandas.Series` drops ``inf`` values.

    Examples
    --------
    >>> from dtoolkit.accessor import DropInfDataFrameAccessor
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
    ...                    "toy": [np.inf, 'Batmobile', 'Bullwhip'],
    ...                    "born": [np.inf, pd.Timestamp("1940-04-25"),
    ...                             -np.inf]})
    >>> df
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Drop the rows where at least one element is inf and -inf.

    >>> df.dropinf()
         name        toy                 born
    1  Batman  Batmobile  1940-04-25 00:00:00

    Drop the columns where at least one element is inf and -inf.

    >>> df.dropinf(axis='columns')
            name
    0    Alfred
    1    Batman
    2  Catwoman

    Drop the rows where all elements are inf and -inf.

    >>> df.dropinf(how='all')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Drop the rows where at least one element is -inf.

    >>> df.dropinf(inf='neg')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00

    Define in which columns to look for inf and -inf values.

    >>> df.dropinf(subset=['name', 'toy'])
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Keep the DataFrame with valid entries in the same variable.

    >>> df.dropinf(inplace=True)
    >>> df
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    """

    def __call__(
        self,
        axis: int | str = 0,
        how: str = "any",
        inf: str = "all",
        subset: list[str] | None = None,
        inplace: bool = False,
    ) -> pd.DataFrame | None:
        inplace = self._validate_inplace(inplace)
        axis = self._validate_axis(axis)
        agg_axis = 1 - axis
        agg_obj = self.pd_obj
        if subset is not None:
            ax = self.pd_obj._get_axis(agg_axis)
            indices = ax.get_indexer_for(subset)
            check = indices == -1
            if check.any():
                raise KeyError(list(np.compress(check, subset)))

            agg_obj = self.pd_obj.take(indices, axis=agg_axis)

        inf_range = _get_inf_range(inf)
        mask = agg_obj.isin(inf_range)
        mask = _get_mask(how, mask, agg_axis)
        result = self.pd_obj.loc(axis=axis)[~mask]

        if not inplace:
            return result

        self.pd_obj._update_inplace(result)


@register_dataframe_accessor("filterin")
class FilterInAccessor(DataFrameAccessor):
    """
    Filter :obj:`~pandas.DataFrame` contents.

    Simlar to :meth:`~pandas.DataFrame.isin`, but the return is value not
    bool.

    Parameters
    ----------
    condition : iterable, Series, DataFrame or dict
        The result will only be true at a location if all the labels match.

        * If ``condition`` is a :obj:`dict`, the keys must be the row/column
          names, which must match. And ``how`` only works on these gave keys.

            - ``axis`` is 0 or 'index', keys would be recognize as column
              names.
            - ``axis`` is 1 or 'columns', keys would be recognize as index
              names.

        * If ``condition`` is a :obj:`~pandas.Series`, that's the index.

        * If ``condition`` is a :obj:`~pandas.DataFrame`, then both the index
          and column labels must match.

    axis : {0 or 'index', 1 or 'columns'}, default 0
        Determine if rows or columns which contain value are filtered.

        * 0, or 'index' : Filter rows which contain value.
        * 1, or 'columns' : Filter columns which contain value.

    how : {'any', 'all'}, default 'all'
        Determine if row or column is filtered from :obj:`~pandas.DataFrame`,
        when we have at least one value or all value.

        * 'any' : If any values are present, filter that row or column.
        * 'all' : If all values are present, filter that row or column.

    inplace : bool, default is False
        If True, do operation inplace and return None.

    Returns
    -------
    DataFrame

    See Also
    --------
    pandas.DataFrame.isin : Whether each element in the DataFrame is contained
        in values.
    pandas.DataFrame.filter : Subset the dataframe rows or columns according
        to the specified index labels.

    Examples
    --------
    >>> from dtoolkit.accessor import FilterInAccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({'num_legs': [2, 4, 2], 'num_wings': [2, 0, 0]},
    ...                   index=['falcon', 'dog', 'cat'])
    >>> df
            num_legs  num_wings
    falcon         2          2
    dog            4          0
    cat            2          0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> df.filterin([0, 2])
            num_legs  num_wings
    falcon         2          2
    cat            2          0

    Filter columns.

    >>> df.filterin([0, 2], axis=1)
                num_wings
    falcon          2
    dog             0
    cat             0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    row/column (depend on ``axis``) separately.

    Filter rows, to check under the column (key) whether contains the value.

    >>> df.filterin({'num_legs': [2], 'num_wings': [2]})
            num_legs  num_wings
    falcon         2          2

    Filter columns, to check under the index (key) whether contains the value.

    >>> df.filterin({'cat': [2]}, axis=1)
            num_legs
    falcon         2
    dog            4
    cat            2

    When ``values`` is a Series or DataFrame the index and column must match.
    Note that 'spider' doesn't match based on the number of legs in ``other``.

    >>> other = pd.DataFrame({'num_legs': [8, 2], 'num_wings': [0, 2]},
    ...                      index=['spider', 'falcon'])
    >>> other
            num_legs  num_wings
    spider         8          0
    falcon         2          2
    >>> df.filterin(other)
            num_legs  num_wings
    falcon         2          2
    """

    def __call__(
        self,
        condition: Iterable | pd.Serie | pd.DataFrame | dict[str, list[str]],
        axis: int | str = 0,
        how: str = "all",
        inplace: bool = False,
    ) -> pd.DataFrame | None:
        inplace = self._validate_inplace(inplace)

        axis = self._validate_axis(axis)
        another_axis = 1 - axis

        mask = self.isin(condition, axis)
        if isinstance(condition, dict):
            # 'how' only works on condition's keys
            names = condition.keys()
            mask = mask[names] if axis == 0 else mask.loc[names]
        mask = _get_mask(how, mask, another_axis)

        result = self.pd_obj.loc(axis=axis)[mask]
        if not inplace:
            return result

        self.pd_obj._update_inplace(result)


def _get_mask(
    how: str,
    mask: pd.DataFrame | np.ndarray,
    axis: int,
) -> pd.Series | np.ndarray:
    return multi_if_else(
        [
            (how == "any", mask.any(axis=axis)),
            (how == "all", mask.all(axis=axis)),
            (how is not None, ValueError(f"invalid inf option: {how}")),
        ],
        TypeError("must specify how"),
    )


@register_dataframe_accessor("repeat")
class RepeatAccessor(DataFrameAccessor):
    """
    Repeat row or column of a :obj:`~pandas.DataFrame`.

    Returns a new DataFrame where each row/column is repeated
    consecutively a given number of times.

    Parameters
    ----------
    repeats : int or array of ints
        The number of repetitions for each element. This should be a
        non-negative integer. Repeating 0 times will return an empty
        :obj:`~pandas.DataFrame`.

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
    >>> from dtoolkit.accessor import RepeatAccessor
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
    """

    def __call__(
        self,
        repeats: int | list[int],
        axis: int | str = 0,
    ) -> pd.DataFrame | None:
        new_index = self.pd_obj.index.copy()
        new_column = self.pd_obj.columns.copy()

        axis = self._validate_axis(axis)
        if axis == 0:
            new_index = new_index.repeat(repeats)
        elif axis == 1:
            new_column = new_column.repeat(repeats)

        new_values = np.repeat(
            self.pd_obj._values,
            repeats,
            axis=axis,
        )
        return pd.DataFrame(
            new_values,
            index=new_index,
            columns=new_column,
        )
