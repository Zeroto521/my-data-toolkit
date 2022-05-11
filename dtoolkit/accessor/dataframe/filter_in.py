from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor._util import get_mask
from dtoolkit.accessor._util import isin
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.util._decorator import deprecated_kwargs


if TYPE_CHECKING:
    from typing import Iterable

    from dtoolkit._typing import IntOrStr


@register_dataframe_method
@deprecated_kwargs(
    "inplace",
    "axis",
    message=(
        "The keyword argument '{argument}' of '{func_name}' is deprecated and will "
        "be removed in 0.0.16. If want to filter columns please use '.T' firstly. "
        "(Warning added DToolKit 0.0.15)"
    ),
)
def filter_in(
    df: pd.DataFrame,
    condition: Iterable | pd.Series | pd.DataFrame | dict[str, list[str]],
    axis: IntOrStr = 0,
    how: str = "all",
    inplace: bool = False,
) -> pd.DataFrame | None:
    """
    Filter :obj:`~pandas.DataFrame` contents.

    Similar to :meth:`~pandas.DataFrame.isin`, but the return is value not
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

        .. deprecated:: 0.0.15
            The ``axis`` is deprecated and will be removed in 0.0.16. If want to
            filter columns please use ``.T`` firstly. (Warning added DToolKit 0.0.15)

    how : {'any', 'all'}, default 'all'
        Determine if row or column is filtered from :obj:`~pandas.DataFrame`,
        when we have at least one value or all value.

        * 'any' : If any values are present, filter that row or column.
        * 'all' : If all values are present, filter that row or column.

    inplace : bool, default is False
        If True, do operation inplace and return None.

        .. deprecated:: 0.0.15
            The ``inplace`` is deprecated and will be removed in 0.0.16.
            (Warning added DToolKit 0.0.15)

    Returns
    -------
    DataFrame

    See Also
    --------
    pandas.DataFrame.isin
        Whether each element in the DataFrame is contained in values.
    pandas.DataFrame.filter
        Subset the dataframe rows or columns according to the specified index
        labels.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         'num_legs': [2, 4, 2],
    ...         'num_wings': [2, 0, 0],
    ...     },
    ...     index=['falcon', 'dog', 'cat'],
    ... )
    >>> df
            num_legs  num_wings
    falcon         2          2
    dog            4          0
    cat            2          0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> df.filter_in([0, 2])
            num_legs  num_wings
    falcon         2          2
    cat            2          0

    Filter columns.

    >>> df.filter_in([0, 2], axis=1)
                num_wings
    falcon          2
    dog             0
    cat             0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    row/column (depend on ``axis``) separately.

    Filter rows, to check under the column (key) whether contains the value.

    >>> df.filter_in({'num_legs': [2], 'num_wings': [2]})
            num_legs  num_wings
    falcon         2          2

    Filter columns, to check under the index (key) whether contains the value.

    >>> df.filter_in({'cat': [2]}, axis=1)
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
    >>> df.filter_in(other)
            num_legs  num_wings
    falcon         2          2
    """

    inplace = validate_bool_kwarg(inplace, "inplace")
    axis = df._get_axis_number(axis)

    another_axis = 1 - axis

    mask = isin(df, condition, axis)
    if isinstance(condition, dict):
        # 'how' only works on condition's keys
        names = condition.keys()
        mask = mask[names] if axis == 0 else mask.loc[names]
    mask = get_mask(how, mask, another_axis)

    result = df.loc(axis=axis)[mask]
    if not inplace:
        return result

    df._update_inplace(result)
