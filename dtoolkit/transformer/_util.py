from __future__ import annotations

import numpy as np
import pandas as pd

from dtoolkit._typing import SeriesOrFrame
from dtoolkit._typing import TwoDimArray
from dtoolkit.accessor.dataframe import to_series  # noqa: F401


def transform_array_to_frame(
    array: np.ndarray,
    frame: SeriesOrFrame,
) -> np.ndarray | SeriesOrFrame:
    """
    Transform ``array``'s :obj:`type` (:obj:`~numpy.ndarray`) to
    :obj:`type` (:obj:`~pandas.Series` or :obj:`~pandas.DataFrame`).

    Parameters
    ----------
    array : array-like of shape ``(n_samples, n_features)``
    frame : Series or DataFrame

    Returns
    -------
    Series, DataFrame or ndarray
    """

    if (
        isinstance(array, (pd.Series, pd.DataFrame))
        or not isinstance(frame, (pd.Series, pd.DataFrame))
        or array.ndim > 2
    ):
        return array

    # Only length is equal
    # sparse matrix can't use `len`
    if array.shape[0] == frame.shape[0] and (
        array.ndim == 1 or (array.ndim == 2 and array.shape[1] == 1)
    ):
        if isinstance(frame, pd.Series):
            name = frame.name
        elif isinstance(frame, pd.DataFrame) and len(frame.columns) == 1:
            name = frame.columns[0]
        else:
            name = None

        return pd.Series(np.ravel(array), index=frame.index, name=name)

    # Both width and length are equal
    elif array.ndim == 2 and array.shape == frame.shape:
        return pd.DataFrame(array, columns=frame.columns, index=frame.index)

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


def transform_frame_to_series(
    X: np.ndarray | SeriesOrFrame,
    drop_name: bool = False,
) -> np.ndarray | SeriesOrFrame:
    """
    Transform ``X`` to Series if ``X`` is one column DataFrame.

    Parameters
    ----------
    X : ndarray, Series or DataFrame
    drop_name : bool

    Returns
    -------
    ndarray, Series or DataFrame
    """

    if isinstance(X, pd.DataFrame):
        X = X.to_series()

    return X.rename() if drop_name and isinstance(X, pd.Series) else X


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
