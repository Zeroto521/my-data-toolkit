from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def drop_inf(s: pd.Series, inf: Literal["all", "pos", "neg"] = "all") -> pd.Series:
    """
    Remove ``inf`` values.

    Parameters
    ----------
    inf : {'all', 'pos', '+', 'neg', '-'}, default 'all'

        * 'all' : Remove ``inf`` and ``-inf``.
        * 'pos' / '+' : Only remove ``inf``.
        * 'neg' / '-' : Only remove ``-inf``.

    Returns
    -------
    Series
        Series with ``inf`` entries dropped from it.

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
    """

    inf_range = get_inf_range(inf)
    mask = s.isin(inf_range)

    return s[~mask]


def get_inf_range(inf: Literal["all", "pos", "neg"] = "all") -> list[float]:
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
