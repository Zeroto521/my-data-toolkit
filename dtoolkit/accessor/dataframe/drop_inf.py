from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.util._validators import validate_bool_kwarg

from dtoolkit._typing import IntOrStr
from dtoolkit.accessor.dataframe import boolean  # noqa
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series.drop_inf import get_inf_range
from dtoolkit.util._decorator import deprecated_kwargs


@register_dataframe_method
@deprecated_kwargs(
    "inplace",
    message=(
        "The keyword argument '{argument}' of '{func_name}' is deprecated and will "
        "be removed in 0.0.17. (Warning added DToolKit 0.0.16)"
    ),
)
def drop_inf(
    df: pd.DataFrame,
    axis: IntOrStr = 0,
    how: str = "any",
    inf: str = "all",
    subset: list[str] = None,
    inplace: bool = False,
) -> pd.DataFrame | None:
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

    inf : {'all', 'pos', '+', 'neg', '-'}, default 'all'
        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' / '+' : Only remove ``inf``.
        * 'neg' / '-' : Only remove ``-inf``.

    subset : array-like, optional
        Labels along other axis to consider, e.g. if you are dropping rows
        these would be a list of columns to include.

    inplace : bool, default False
        If True, do operation inplace and return None.

        .. deprecated:: 0.0.17
            'inplace' is deprecated and will be removed in 0.0.17.
            (Warning added DToolKit 0.0.16)

    Returns
    -------
    DataFrame or None
        DataFrame with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    dtoolkit.accessor.series.drop_inf
        :obj:`~pandas.Series` drops ``inf`` values.

    Examples
    --------
    >>> import dtoolkit.accessor
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

    >>> df.drop_inf()
         name        toy                 born
    1  Batman  Batmobile  1940-04-25 00:00:00

    Drop the columns where at least one element is inf and -inf.

    >>> df.drop_inf(axis='columns')
           name
    0    Alfred
    1    Batman
    2  Catwoman

    Drop the rows where all elements are inf and -inf.

    >>> df.drop_inf(how='all')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Drop the rows where at least one element is -inf.

    >>> df.drop_inf(inf='neg')
           name        toy                 born
    0    Alfred        inf                  inf
    1    Batman  Batmobile  1940-04-25 00:00:00

    Define in which columns to look for inf and -inf values.

    >>> df.drop_inf(subset=['name', 'toy'])
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    2  Catwoman   Bullwhip                 -inf

    Keep the DataFrame with valid entries in the same variable.

    >>> df.drop_inf(inplace=True)
    >>> df
           name        toy                 born
    1    Batman  Batmobile  1940-04-25 00:00:00
    """

    inplace = validate_bool_kwarg(inplace, "inplace")
    inf_range = get_inf_range(inf)
    axis = df._get_axis_number(axis)
    agg_axis = 1 - axis

    agg_obj = df
    if subset is not None:
        ax = df._get_axis(agg_axis)
        indices = ax.get_indexer_for(subset)
        check = indices == -1
        if check.any():
            raise KeyError(list(np.compress(check, subset)))

        agg_obj = df.take(indices, axis=agg_axis)

    mask = agg_obj.isin(inf_range).boolean(how=how, axis=agg_axis)
    result = df.loc(axis=axis)[~mask]

    if not inplace:
        return result

    df._update_inplace(result)
