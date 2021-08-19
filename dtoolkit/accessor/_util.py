from __future__ import annotations

import numpy as np
import pandas as pd

from ..util import multi_if_else


def validate_axis(df: pd.DataFrame, axis: int | str) -> int:
    if isinstance(axis, (tuple, list)):
        msg = "supplying multiple axes to axis is no longer supported."
        raise TypeError(msg)

    return df._get_axis_number(axis)


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


def get_mask(
    how: str,
    mask: pd.DataFrame | np.ndarray,
    axis: int,
) -> pd.Series | np.ndarray:
    return multi_if_else(
        [
            (how == "any", mask.any(axis=axis)),
            (how == "all", mask.all(axis=axis)),
            (how is not None, ValueError(f"invalid inf option: {how}")),
        ],
        TypeError("must specify how"),
    )
