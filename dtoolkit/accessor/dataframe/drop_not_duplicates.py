from collections.abc import Hashable
from typing import Literal
from typing import Sequence

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def drop_not_duplicates(
    df: pd.DataFrame,
    /,
    subset: Hashable | Sequence[Hashable] | None = None,
    keep: Literal["first", "last", False] = False,
) -> pd.DataFrame:
    """
    Return duplicate DataFrame values.

    A sugary syntax wraps :meth:`~pandas.DataFrame.duplicated`::

        df[df.duplicated(subset=subset, keep=keep)]

    Parameters
    ----------
    subset : column label or sequence of labels, optional
        Only consider certain columns for identifying duplicates, by default use all of
        the columns.

    keep : {'first', 'last', False}, default ``False``
        Method to handle duplicates:

        - 'first' : Keep duplicates except for the first occurrence.
        - 'last' : Keep duplicates except for the last occurrence.
        - ``False`` : Keep all duplicates.

    Returns
    -------
    DataFrame
        Kept duplicate values.

    See Also
    --------
    pandas.DataFrame.duplicated
    pandas.DataFrame.drop_duplicates
    dtoolkit.accessor.series.drop_not_duplicates

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'brand': ['Yum Yum', 'Yum Yum', 'Indomie', 'Indomie', 'Indomie'],
    ...     'style': ['cup', 'cup', 'cup', 'pack', 'pack'],
    ...     'rating': [4, 4, 3.5, 15, 5]
    ... })
    >>> df
         brand style  rating
    0  Yum Yum   cup     4.0
    1  Yum Yum   cup     4.0
    2  Indomie   cup     3.5
    3  Indomie  pack    15.0
    4  Indomie  pack     5.0
    >>> df.drop_not_duplicates(subset='rating')
         brand style  rating
    0  Yum Yum   cup     4.0
    1  Yum Yum   cup     4.0
    """

    return df[df.duplicated(subset=subset, keep=keep)]
