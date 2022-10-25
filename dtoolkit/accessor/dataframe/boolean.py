from __future__ import annotations

from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def boolean(
    df: pd.DataFrame,
    /,
    how: Literal["any", "all"] = "any",
    complement: bool = False,
    **kwargs,
) -> pd.Series:
    """
    Return whether any (or all) element is True, potentially over an ``axis``.

    An API to gather :meth:`~pandas.DataFrame.any` and
    :meth:`~pandas.DataFrame.all` to one.

    Parameters
    ----------
    how : {'any', 'all'}, default 'any'
        Choose a method to get mask.

        * 'any' : Do :meth:`~pandas.DataFrame.any` function to DataFrame.
        * 'all' : Do :meth:`~pandas.DataFrame.all` function to DataFrame.

    axis : {0 or 'index', 1 or 'columns', None}, default 0
        Indicate which axis or axes should be reduced.

        * 0 / 'index' : reduce the index, return a Series whose index is
          the original column labels.

        * 1 / 'columns' : reduce the columns, return a Series whose index is
          the original index.

        * None : reduce all axes, return a scalar.

    complement : bool, default False
        If True does logical 'not' operator to values firstly.

    **kwargs
        See the documentation for :meth:`~pandas.DataFrame.any` and
        :attr:`~pandas.DataFrame.all` for complete details on the keyword arguments.

    Returns
    -------
    Series

    Raises
    ------
    ValueError
        If ``how`` isn't "any" or "all".

    See Also
    --------
    pandas.DataFrame.any
    pandas.DataFrame.all

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [True, True, False], "b": [False, True, False]})
    >>> df
           a      b
    0   True  False
    1   True   True
    2  False  False

    Get the bool value from each column.

    >>> df.boolean(how="any")
    a    True
    b    True
    dtype: bool

    Get the bool value from each row. And require each element is True.

    >>> df.boolean(how="all", axis=1)
    0    False
    1     True
    2    False
    dtype: bool

    Do a '~' (logical not) operation then get the bool value.

    >>> df.boolean(how="all", axis=1, complement=True)
    0    False
    1    False
    2     True
    dtype: bool

    Get the bool value from the entire data.

    >>> df.boolean(how="all", axis=None)
    False
    """

    if how not in {"any", "all"}:
        raise ValueError(f"invalid how option: {how!r}")

    return getattr(~df if complement else df, how)(**kwargs)
