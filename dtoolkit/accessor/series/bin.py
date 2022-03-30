from __future__ import annotations

import pandas as pd
from pandas.util._validators import validate_bool_kwarg

from dtoolkit.accessor.register import register_series_method


@register_series_method
def bin(
    s: pd.Series,
    bins,
    labels=None,
    right: bool = True,
    retbins: bool = False,
    precision: int = 3,
    include_lowest: bool = False,
    duplicates: str = "raise",
    ordered: bool = False,
    inplace: bool = False,
) -> pd.Series | None:
    """
    Bin values into discrete intervals.

    See Also
    --------
    pandas.cut: This accessor's prototype method.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    Create **score** samples:

    >>> s = pd.Series([100, 10, 50, 20, 90, 60])

    Bin score to rank level:

        - (0, 60] -> E
        - (60, 70] -> D
        - (70, 80] -> C
        - (80, 90] -> B
        - (90, 100] -> A

    >>> s.bin([0, 60, 70, 80, 90, 100], ['E', 'D', 'C', 'B', 'A'], right=True)
    0    A
    1    E
    2    E
    3    E
    4    B
    5    E
    dtype: category
    Categories (5, object): ['E', 'D', 'C', 'B', 'A']
    """
    inplace = validate_bool_kwarg(inplace, "inplace")

    result = pd.cut(
        s,
        bins=bins,
        right=right,
        labels=labels,
        retbins=retbins,
        precision=precision,
        include_lowest=include_lowest,
        duplicates=duplicates,
        ordered=ordered,
    )

    if not inplace:
        return result

    s._update_inplace(result)
