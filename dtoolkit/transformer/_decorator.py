from functools import wraps

from ._util import transform_array_to_frame


def frame_in_frame_out(func):
    """
    Wrap :func:`~dtoolkit.transformer._util.transform_array_to_frame` to
    decorator.
    """

    @wraps(func)
    def decorator(self, X):
        X_new = func(self, X)

        return transform_array_to_frame(X_new, X)

    return decorator
