from __future__ import annotations

import numpy as np
import pandas as pd

from dtoolkit._typing import OneDimArray
from dtoolkit._typing import SeriesOrFrame
from dtoolkit._typing import TwoDimArray


def transform_array_to_frame(
    array: np.ndarray,
    frame: pd.DataFrame,
) -> TwoDimArray:
    """
    Transform ``array``'s :obj:`type` (:obj:`~numpy.ndarray`) to
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

    if isinstance(frame, pd.DataFrame) and np.shape(array) == np.shape(frame):
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

    return X.to_frame() if isinstance(X, pd.Series) else X


def transform_frame_to_series(X: np.ndarray | SeriesOrFrame) -> OneDimArray:
    """
    Transform ``X`` to Series if ``X`` is one column DataFrame.

    Parameters
    ----------
    X : ndarray, Series or DataFrame

    Returns
    -------
    Series or ndarray
    """

    return X.to_series() if isinstance(X, pd.DataFrame) else X


def snake_to_camel(name: str) -> str:
    """
    Change snake style name to camel style name.

    Parameters
    ----------
    name : str
        Snake style name

    Returns
    -------
    str
        Camel style name

    Examples
    --------
    >>> from dtoolkit.transformer._util import snake_to_camel
    >>> snake_to_camel(snake_to_camel.__name__)
    'SnakeToCamel'
    """

    components = name.split("_")
    components = (x.title() for x in components)
    return "".join(components)
