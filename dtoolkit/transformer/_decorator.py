from functools import wraps

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
