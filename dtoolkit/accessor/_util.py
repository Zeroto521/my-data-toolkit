from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
import pandas as pd

from dtoolkit._typing import OneDimArray
from dtoolkit._typing import SeriesOrFrame
from dtoolkit._typing import TwoDimArray
from dtoolkit.util import multi_if_else


def get_inf_range(inf: str = "all") -> list[float]:
    return multi_if_else(
        [
            (inf == "all", [np.inf, -np.inf]),
            (inf == "pos", [np.inf]),
            (inf == "neg", [-np.inf]),
            (inf is not None, ValueError(f"invalid inf option: {inf}")),
        ],
        TypeError("must specify inf"),
    )


def get_mask(how: str, mask: TwoDimArray, axis: int) -> OneDimArray:
    return multi_if_else(
        [
            (how == "any", mask.any(axis=axis)),
            (how == "all", mask.all(axis=axis)),
            (how is not None, ValueError(f"invalid inf option: {how}")),
        ],
        TypeError("must specify how"),
    )


def isin(
    df: pd.DataFrame,
    values: Iterable | SeriesOrFrame | dict[str, list[str]],
    axis: int | str = 0,
) -> pd.DataFrame:
    """
    Extend :meth:`~pandas.DataFrame.isin` function. When ``values`` is
    :obj:`dict` and ``axis`` is 1, ``values``' key could be index name.
    """

    axis = df._get_axis_number(axis)

    if isinstance(values, dict) and axis == 1:
        values = defaultdict(list, values)
        result = (df.iloc[[r]].isin(values[i]) for r, i in enumerate(df.index))
        return pd.concat(result, axis=0)

    return df.isin(values)
