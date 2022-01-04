from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from dtoolkit._typing import SeriesOrFrame
    from dtoolkit._typing import TwoDimArray


def transform_array_to_frame(
    array: np.ndarray,
    frame: pd.DataFrame,
) -> TwoDimArray:
    """
    Transform ``array``'s :obj:`type` (:obj:`~numpy.ndarray`) to
    `
    :obj:`type` (:obj:`~pandas.DataFrame`).

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


def transform_series_to_frame(X: np.ndarray | SeriesOrFrame) -> TwoDimArray:
    """
    Transform ``X`` to DataFrame if ``X`` type is Series.

    Parameters
    ----------
    X : ndarray, Series or DataFrame

    Returns
    -------
    DataFrame or ndarray
    """

    if isinstance(X, pd.Series):
        return X.to_frame()

    return X
