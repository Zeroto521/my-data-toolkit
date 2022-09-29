from __future__ import annotations

from typing import Hashable
from typing import Iterable
from typing import Literal

import pandas as pd

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.accessor.dataframe import boolean  # noqa: F401
from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def filter_in(
    df: pd.DataFrame,
    condition: Iterable | SeriesOrFrame | dict[Hashable, list[Hashable]],
    /,
    how: Literal["any", "all"] = "all",
    complement: bool = False,
) -> pd.DataFrame:
    """
    Filter :obj:`~pandas.DataFrame` contents.

    Similar to :meth:`~pandas.DataFrame.isin`, but the return is not bool.

    Parameters
    ----------
    condition : Iterable, Series, DataFrame or dict
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

    complement : bool, default is False
        If True, do operation reversely.

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

    dtoolkit.accessor.series.filter_in
        Filter Series contents.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         'legs': [2, 4, 2],
    ...         'wings': [2, 0, 0],
    ...     },
    ...     index=['falcon', 'dog', 'cat'],
    ... )
    >>> df
            legs  wings
    falcon     2      2
    dog        4      0
    cat        2      0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> df.filter_in([0, 2])
            legs  wings
    falcon     2      2
    cat        2      0

    Filter any row doesn't contain 0 or 2.

    >>> df.filter_in([0, 2], how="any", complement=True)
            legs  wings
    dog        4      0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    column separately.

    >>> df.filter_in({'legs': [2], 'wings': [2]})
            legs  wings
    falcon     2      2

    When ``values`` is a Series or DataFrame the index and column must be matched.
    Note that 'spider' doesn't match based on the number of legs in ``other``.

    >>> other = pd.DataFrame(
    ...     {
    ...         'legs': [8, 2],
    ...         'wings': [0, 2],
    ...     },
    ...     index=['spider', 'falcon'],
    ... )
    >>> other
            legs  wings
    spider     8      0
    falcon     2      2
    >>> df.filter_in(other)
            legs  wings
    falcon     2      2
    """

    return df[
        select_column(df, condition=condition)
        .isin(condition)
        .boolean(
            how=how,
            axis=1,
            complement=complement,
        )
    ]


def select_column(
    df: pd.DataFrame,
    /,
    condition: Iterable | SeriesOrFrame | dict[Hashable, list[Hashable]],
) -> pd.DataFrame:
    """Select DataFram columns via condition type"""

    if isinstance(condition, dict):
        # 'how' only works on condition these dictionary's keys
        return df[condition.keys()]
    elif isinstance(condition, pd.DataFrame):
        # 'how' only works on condition these DataFrame's columns
        return df[condition.columns]

    return df
