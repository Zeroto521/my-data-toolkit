from functools import wraps

import pandas as pd

from ._util import transform_array_to_frame
from ._util import transform_series_to_frame


def frame_in_frame_out(wrapped):
    """
    Wrap :func:`~dtoolkit.transformer._util.transform_array_to_frame` to
    decorator.
    """

    @wraps(wrapped)
    def decorator(self, X):
        X_new = wrapped(self, X)

        return transform_array_to_frame(X_new, X)

    return decorator


def force_series_to_frame(wrapped):
    """
    Wrap :func:`~dtoolkit.transformer._util.transform_series_to_frame` to
    decorator.
    """

    @wraps(wrapped)
    def decorator(self, X):
        X_new = transform_series_to_frame(X)

        return wrapped(self, X_new)

    return decorator


def require_series_or_frame(wrapped):
    """
    Validate class instance method second parameter data type is a series or
    dataframe.
    """

    @wraps(wrapped)
    def decorator(self, X):
        if not isinstance(X, (pd.Series, pd.DataFrame)):
            raise TypeError(
                f"For argument 'X' expected type 'pandas.Series' or "
                f"'pandas.DataFrame', received type {type(X).__name__}.",
            )

        return wrapped(self, X)

    return decorator
