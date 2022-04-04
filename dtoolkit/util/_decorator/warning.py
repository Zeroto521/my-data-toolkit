from functools import wraps
from warnings import warn


def warning(message: str, category: Exception = None, **kwargs):
    """
    A warning decorator.

    Parameters
    ----------
    message : str
        The warning information to user.

    category : Exception, optional
        If given, must be a **warning category class**. it defaults to
        :keyword:`UserWarning`.

    **kwargs
        See the documentation for :meth:`warnings.warn` for complete details on
        the keyword arguments.

    See Also
    --------
    warnings.warn

    Examples
    --------
    >>> from dtoolkit.util._decorator import warning
    >>> @warning("This's a warning message.")
    ... def func(*args, **kwargs):
    ...     ...
    >>> func()
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            warn(message, category=category, **kwargs)

            return func(*func_args, **func_kwargs)

        return wrapper

    return decorator
