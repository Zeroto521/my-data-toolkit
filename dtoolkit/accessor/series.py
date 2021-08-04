from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.util._validators import validate_bool_kwarg

from .base import Accessor


@register_series_accessor("dropinf")
class DropInfSeriesAccessor(Accessor):
    """
    Remove ``inf`` values.

    Parameters
    ----------
    inf : {'all', 'pos', 'neg'}, default 'all'
        * 'all' : Remove :obj:`~numpy.inf` and -:obj:`~numpy.inf`.
        * 'pos' : Only remove :obj:`~numpy.inf`:.
        * 'neg' : Only remove -:obj:`~numpy.inf`:.

    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    Series or None
        Series with ``inf`` entries dropped from it or None if
        ``inplace=True``.

    See Also
    --------
    DropInfDataFrameAccessor : :obj:`~pandas.DataFram` drops rows or columns
        which contain :obj:`~numpy.inf` values.

    Examples
    --------
    >>> from dtoolkit.accessor import DropInfSeriesAccessor
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

    def __call__(
        self,
        inf: str = "all",
        inplace: bool = False,
    ) -> pd.Series | None:
        inplace = validate_bool_kwarg(inplace, "inplace")

        if inf == "all":
            inf_range = [np.inf, -np.inf]
        elif inf == "pos":
            inf_range = [np.inf]
        elif inf == "neg":
            inf_range = [-np.inf]
        elif inf is not None:
            raise ValueError(f"invalid inf option: {inf}")
        else:
            raise TypeError("must specify inf")

        mask = ~self.pd_obj.isin(inf_range)
        result = self.pd_obj[mask]

        if not inplace:
            return result

        self.pd_obj._update_inplace(result)
