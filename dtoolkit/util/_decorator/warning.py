from functools import wraps
from warnings import warn

from dtoolkit.util._exception import find_stack_level


def warning(
    message: str,
    category: Exception = None,
    stacklevel: int = find_stack_level(),
    **kwargs
):
    """
    A warning decorator.

    Parameters
    ----------
    message : str
        The warning information to user.

    category : Exception, optional
        If given, must be a **warning category class**. it defaults to
        :exc:`UserWarning`.

    stacklevel : int
        Default to find the first place in the stack that is not inside dtoolkit.

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
        def wrapper(*f_args, **f_kwargs):
            warn(message, category=category, stacklevel=stacklevel, **kwargs)

            return func(*f_args, **f_kwargs)

        return wrapper

    return decorator
