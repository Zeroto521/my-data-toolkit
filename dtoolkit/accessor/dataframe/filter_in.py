from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.dataframe import boolean  # noqa
from dtoolkit.accessor.register import register_dataframe_method


if TYPE_CHECKING:
    from typing import Iterable


@register_dataframe_method
def filter_in(
    df: pd.DataFrame,
    condition: Iterable | pd.Series | pd.DataFrame | dict[str, list[str]],
    how: str = "all",
) -> pd.DataFrame:
    """
    Filter :obj:`~pandas.DataFrame` contents.

    Similar to :meth:`~pandas.DataFrame.isin`, but the return is value not
    bool.

    Parameters
    ----------
    condition : iterable, Series, DataFrame or dict
        The filtered result is based on this specific condition.

        * If ``condition`` is a :obj:`dict`, the keys must be the column
          names, which must be matched. And ``how`` only works on these gave keys.

        * If ``condition`` is a :obj:`~pandas.Series`, that's the index.

        * If ``condition`` is a :obj:`~pandas.DataFrame`, then both the index
          and column labels must be matched.

    how : {'any', 'all'}, default 'all'
        Determine whether the row is filtered from :obj:`~pandas.DataFrame`,
        when there have at least one value or all value.

        * 'any' : If any values are present, filter that rows.
        * 'all' : If all values are present, filter that rows.

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

    >>> df.T.filter_in([0, 2])
               falcon  dog  cat
    num_wings       2    0    0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    column separately.

    >>> df.filter_in({'num_legs': [2], 'num_wings': [2]})
            num_legs  num_wings
    falcon         2          2

    When ``values`` is a Series or DataFrame the index and column must match.
    Note that 'spider' doesn't match based on the number of legs in ``other``.

    >>> other = pd.DataFrame(
    ...     {
    ...         'num_legs': [8, 2],
    ...         'num_wings': [0, 2],
    ...     },
    ...     index=['spider', 'falcon'],
    ... )
    >>> other
            num_legs  num_wings
    spider         8          0
    falcon         2          2
    >>> df.filter_in(other)
            num_legs  num_wings
    falcon         2          2
    """

    mask = df.isin(condition)
    if isinstance(condition, dict):
        # 'how' only works on condition's keys
        mask = mask[condition.keys()]

    return df[mask.boolean(how=how, axis=1)]
