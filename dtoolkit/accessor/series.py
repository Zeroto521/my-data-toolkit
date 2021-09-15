from __future__ import annotations

from textwrap import dedent
from typing import Any

import pandas as pd
from pandas.util._decorators import doc
from pandas.util._validators import validate_bool_kwarg

from ..util.generic import multi_if_else
from ._util import between
from ._util import get_inf_range
from .register import register_series_method

__all__ = ["cols", "dropinf"]


@register_series_method
@doc(
    returns=dedent(
        """
    Returns
    -------
    str
        The name of the Series.
    """,
    ),
)
def cols(s: pd.Series) -> str:
    """
    A API to gather :attr:`~pandas.Series.name` and
    :attr:`~pandas.DataFrame.columns` to one.
    {returns}
    See Also
    --------
    pandas.Series.name
    pandas.DataFrame.columns

    Examples
    --------
    >>> from dtoolkit.accessor.dataframe import cols
    >>> from dtoolkit.accessor.series import cols
    >>> import pandas as pd

    Get :attr:`~pandas.Series.name`.

    >>> s = pd.Series(range(10), name="item")
    >>> s.cols()
    'item'

    Get :attr:`~pandas.DataFrame.columns`.

    >>> d = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}})
    >>> d.cols()
    ['a', 'b']
    """

    return s.name


@register_series_method
def dropinf(
    s: pd.Series,
    inf: str = "all",
    inplace: bool = False,
) -> pd.Series | None:
    """
    Remove ``inf`` values.

    Parameters
    ----------
    inf : {'all', 'pos', 'neg'}, default 'all'
        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' : Only remove ``inf``.
        * 'neg' : Only remove ``-inf``.

    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    Series or None
        Series with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    dtoolkit.accessor.dataframe.dropinf : :obj:`~pandas.DataFrame` drops rows
        or columns which contain ``inf`` values.

    Examples
    --------
    >>> from dtoolkit.accessor.series import dropinf
    >>> import pandas as pd
    >>> import numpy as np
    >>> ser = pd.Series([1., 2., np.inf])
    >>> ser
    0    1.0
    1    2.0
    2    inf
    dtype: float64

    Drop inf values from a Series.

    >>> ser.dropinf()
    0    1.0
    1    2.0
    dtype: float64

    Keep the Series with valid entries in the same variable.

    >>> ser.dropinf(inplace=True)
    >>> ser
    0    1.0
    1    2.0
    dtype: float64
    """

    inplace = validate_bool_kwarg(inplace, "inplace")
    inf_range = get_inf_range(inf)
    mask = s.isin(inf_range)
    result = s[~mask]

    if not inplace:
        return result

    s._update_inplace(result)


@register_series_method
def range_replace(
    s: pd.DataFrame,
    to_replace: dict[tuple, Any],
    equal_sign: str = "left",
    inplace: bool = False,
) -> pd.Series | None:
    result = s.apply(
        lambda value: multi_if_else(
            if_condition_return=(
                (
                    between(
                        value,
                        *left_right,
                        equal_sign=equal_sign,
                    ),
                    label,
                )
                for left_right, label in to_replace.items()
            ),
            else_return=value,
        ),
    )

    if not inplace:
        return result

    s._update_inplace(result)
