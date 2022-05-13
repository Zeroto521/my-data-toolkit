from __future__ import annotations

from functools import wraps
from warnings import warn

from dtoolkit.util._exception import find_stack_level


def deprecated_kwargs(
    *arguments: list[str],
    message: str = "The keyword argument '{argument}' of '{func_name}' is deprecated.",
):
    """
    Used as a decorator when deprecating function keyword argument names.

    Parameters
    -----------
    arguments : list of str
        The list of deprecated keyword arguments.

    message : str
        The message of :exc:`DeprecationWarning`. It should be a string or a
        string template. If a string template defaults input ``func_name`` and
        ``argument``.

    Raises
    ------
    DeprecationWarning
        If one of `arguments` is input into the function.

    See Also
    --------
    dtoolkit.util._decorator.warning
    dtoolkit.util._decorator.deprecated_alias

    Examples
    --------
    >>> from dtoolkit.util._decorator import deprecated_kwargs
    >>> @deprecated_kwargs('x', 'y')
    ... def plus(a, b, x=0, y=0):
    ...     return a + b
    >>> plus(1, 2, x=1, y=2)
    3
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for argument in arguments:
                if argument in kwargs:
                    warn(
                        message.format(func_name=func.__name__, argument=argument),
                        DeprecationWarning,
                        find_stack_level(),
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator
