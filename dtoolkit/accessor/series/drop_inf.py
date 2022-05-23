from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor.register import register_series_method
from dtoolkit.util._decorator import deprecated_kwargs


@register_series_method
@deprecated_kwargs(
    "inplace",
    message=(
        "The keyword argument '{argument}' of '{func_name}' is deprecated and will "
        "be removed in 0.0.17. (Warning added DToolKit 0.0.16)"
    ),
)
def drop_inf(
    s: pd.Series,
    inf: str = "all",
    inplace: bool = False,
) -> pd.Series | None:
    """
    Remove ``inf`` values.

    Parameters
    ----------
    inf : {'all', 'pos', '+', 'neg', '-'}, default 'all'

        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' / '+' : Only remove ``inf``.
        * 'neg' / '-' : Only remove ``-inf``.

    inplace : bool, default False
        If True, do operation inplace and return None.

        .. deprecated:: 0.0.17
            'inplace' is deprecated and will be removed in 0.0.17.
            (Warning added DToolKit 0.0.16)

    Returns
    -------
    Series or None
        Series with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    dtoolkit.accessor.dataframe.drop_inf
        :obj:`~pandas.DataFrame` drops rows or columns which contain ``inf``
        values.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> import numpy as np
    >>> s = pd.Series([1., 2., np.inf])
    >>> s
    0    1.0
    1    2.0
    2    inf
    dtype: float64

    Drop inf values from a Series.

    >>> s.drop_inf()
    0    1.0
    1    2.0
    dtype: float64

    Keep the Series with valid entries in the same variable.

    >>> s.drop_inf(inplace=True)
    >>> s
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


def get_inf_range(inf: str = "all") -> list[float]:
    """Get inf value from string"""

    inf_range = {
        "all": [np.inf, -np.inf],
        "pos": [np.inf],
        "+": [np.inf],
        "neg": [-np.inf],
        "-": [-np.inf],
    }

    if inf in inf_range:
        return inf_range[inf]

    raise ValueError(f"invalid inf option: {inf!r}")
