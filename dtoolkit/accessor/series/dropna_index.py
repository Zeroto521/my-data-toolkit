from typing import Literal

import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_series_method


@register_series_method
@doc(klass="Series")
def dropna_index(s: pd.Series, /, how: Literal["any", "all"] = "any") -> pd.Series:
    """
    Return a new {klass} with missing index removed.

    Parameters
    ----------
    how : {{"any", "all"}}, default "any"
        If the ``Index`` is a :class:`~pandas.MultiIndex`, drop the value when "any"
        or "all" levels are NaN.

    Returns
    -------
    {klass}

    Raises
    ------
    ValueError
        If ``how`` isn't "any" or "all".

    See Also
    --------
    pandas.{klass}.dropna
    dtoolkit.accessor.series.dropna_index
    dtoolkit.accessor.dataframe.dropna_index

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}}, index=[None, 0])
    >>> df
         a  b
    NaN  1  3
    0.0  2  4
    >>> df.dropna_index()
         a  b
    0.0  2  4
    """

    if how not in {"any", "all"}:
        raise ValueError(f"invalid how option: {how!r}")

    return s[~s.index._isnan] if s.index.hasnans else s
