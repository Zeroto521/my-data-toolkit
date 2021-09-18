from __future__ import annotations

import pandas as pd


def require_series_or_frame(X: pd.Series | pd.DataFrame):
    """Validate data type is a series or dataframe."""

    if not isinstance(X, (pd.Series, pd.DataFrame)):
        raise TypeError(
            f"For argument 'X' expected type 'pandas.Series' or "
            f"'pandas.DataFrame', received type {type(X).__name__}.",
        )
