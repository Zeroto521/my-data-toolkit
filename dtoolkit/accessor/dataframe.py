from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from pandas.util._validators import validate_bool_kwarg

from .._util import multi_if_else
from .base import Accessor
from .series import _get_inf_range


@register_dataframe_accessor("dropinf")
class DropInfDataFrameAccessor(Accessor):
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
    DropInfSeriesAccessor : :obj:`pandas.Series` drops missing values.

    Examples
    --------
    from dtoolkit.accessor import DropInfDataFrameAccessor
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

        inplace = validate_bool_kwarg(inplace, "inplace")
        if isinstance(axis, (tuple, list)):
            msg = "supplying multiple axes to axis is no longer supported."
            raise TypeError(msg)

        axis = self.pd_obj._get_axis_number(axis)
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
        mask = multi_if_else(
            [
                (how == "any", mask.any(axis=agg_axis)),
                (how == "all", mask.all(axis=agg_axis)),
            ],
            if_condition_raise=[
                (how is not None, ValueError(f"invalid inf option: {how}")),
            ],
            else_raise=TypeError("must specify how"),
        )

        result = self.pd_obj.loc(axis=axis)[~mask]

        if not inplace:
            return result

        self.pd_obj._update_inplace(result)


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
    Repeat row or column of a :obj:`~pandas.DataFrame`.

    Returns a new DataFrame where each row/column
    is repeated consecutively a given number of times.

    Parameters
    ----------
    repeats : int or array of ints
        The number of repetitions for each element. This should be a
        non-negative integer. Repeating 0 times will return an empty
        :obj:`~pandas.DataFrame`.
    axis :  {0, 1}, int
        The axis along which to repeat. By default, along **row** to repeat.

    Returns
    -------
    DataFrame
        Newly created DataFrame with repeated elements.

    See Also
    --------
    numpy.repeat : this transformer's prototype method.

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
        new_index = self.pd_obj.index.copy()
        new_column = self.pd_obj.columns.copy()

        if axis == 0:
            new_index = self.pd_obj.index.repeat(repeats)
        elif axis == 1:
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
