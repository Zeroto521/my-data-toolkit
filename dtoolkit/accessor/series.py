from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.util._validators import validate_bool_kwarg

from .base import Accessor


@register_series_accessor("dropinf")
class DropInfSeriesAccessor(Accessor):
    """
    Return a new :obj:`~pandas.Series` with :obj:`numpy.inf` and
    :obj:`-numpy.inf` values removed.

    Parameters
    ----------
    inplace : bool, default False
        If True, do operation inplace and return None.

    Returns
    -------
    Series or None
        Series with :obj:`~numpy.inf` entries dropped from it or None
        if ``inplace=True``.

    See Also
    --------
    DropInfDataFrameAccessor : Drop rows or columns which contain
        :obj:`~numpy.inf` values.

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

    def __call__(self, inplace: bool = False) -> pd.Series | None:
        inplace = validate_bool_kwarg(inplace, "inplace")

        mask = ~self.pd_obj.isin([np.inf, -np.inf])
        result = self.pd_obj[mask]

        if not inplace:
            return result

        self.pd_obj._update_inplace(result)
