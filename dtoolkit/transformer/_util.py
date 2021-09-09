from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    import numpy as np


def transform_array_to_frame(
    array: np.ndarray,
    frame: pd.DataFrame,
) -> pd.DataFrame | np.ndarray:
    """
    Transform ``array``'s :obj:`type` (:obj:`~numpy.ndarray`) to
    ``frame``'s :obj:`type` (:obj:`~pandas.DataFrame`).

    Parameters
    ----------
    array : array-like of shape ``(n_samples, n_features)``
    frame : DataFrame

    Returns
    -------
    DataFrame or ndarray
        DataFrame if ``frame`` is DataFrame else ndarray.
    """

    if isinstance(frame, pd.DataFrame):
        return pd.DataFrame(
            array,
            columns=frame.columns,
            index=frame.index,
        )

    return array
