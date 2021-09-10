from functools import wraps

from ._util import transform_array_to_frame


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
