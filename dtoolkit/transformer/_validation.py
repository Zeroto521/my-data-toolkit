import pandas as pd

from dtoolkit._typing import SeriesOrFrame


def require_series_or_frame(X: SeriesOrFrame):
    """Validate data type is a series or dataframe."""

    if not isinstance(X, (pd.Series, pd.DataFrame)):
        raise TypeError(
            f"For argument 'X' expected type 'pandas.Series' or "
            f"'pandas.DataFrame', received type {type(X).__name__!r}.",
        )
