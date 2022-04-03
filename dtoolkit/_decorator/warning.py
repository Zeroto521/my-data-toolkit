from functools import wraps
from warnings import warn


def warning(message: str, category: Exception = None):
    """
    A warning decorator.

    Parameters
    ----------
    message : str
        The warning information to user.

    category : Exception, optional
        If given, must be a **warning category class**. it defaults to
        :keyword:`UserWarning`.

    See Also
    --------
    warnings.warn

    Examples
    --------
    >>> from dtoolkit._decorator import warning
    >>> @warning("This's a warning message.")
    ... def func() -> str:
    ...     return "[Done]."
    >>> func()
    '[Done].'
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warn(message, category=category)

            return func(*args, **kwargs)

        return wrapper

    return decorator
