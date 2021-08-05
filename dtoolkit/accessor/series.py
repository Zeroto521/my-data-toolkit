from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.util._validators import validate_bool_kwarg

from .._util import multi_if_else
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

        inf_range = _get_inf_range(inf)
        mask = self.pd_obj.isin(inf_range)
        result = self.pd_obj[~mask]

        if not inplace:
            return result

        self.pd_obj._update_inplace(result)


def _get_inf_range(inf: str = "all") -> list[float]:

    return multi_if_else(
        [
            (inf == "all", [np.inf, -np.inf]),
            (inf == "pos", [np.inf]),
            (inf == "neg", [-np.inf]),
        ],
        if_condition_raise=[
            (inf is not None, ValueError(f"invalid inf option: {inf}")),
        ],
        else_raise=TypeError("must specify inf"),
    )
