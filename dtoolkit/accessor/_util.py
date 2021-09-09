from __future__ import annotations

from typing import TYPE_CHECKING

from ..util import multi_if_else

if TYPE_CHECKING:
    import pandas as pd
    import numpy as np


def get_inf_range(inf: str = "all") -> list[float]:
    infinity = float("inf")

    return multi_if_else(
        [
            (inf == "all", [infinity, -infinity]),
            (inf == "pos", [infinity]),
            (inf == "neg", [-infinity]),
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
