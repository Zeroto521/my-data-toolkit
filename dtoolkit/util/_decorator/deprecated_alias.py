from functools import wraps
from warnings import warn

from dtoolkit.util._exception import find_stack_level


# based on https://stackoverflow.com/a/49802489/9155078
def deprecated_alias(
    warning_msg: str = (
        "'{func_name}'s paramerter '{old_alias}' is deprecated, "
        "please use the parameter '{new_alias}'."
    ),
    error_msg: str = (
        "'{func_name}' shouldn't received both '{old_alias}' "
        "and '{new_alias}' parameters at the same time."
    ),
    **aliases,
):
    """
    Used as a decorator when deprecating old function argument names, while keeping
    backwards compatibility.

    Parameters
    -----------
    warning_msg : str
        The message of :exc:`DeprecationWarning`. It should be a string or a
        string template. If a string template defaults input ``func_name``,
        ``old_alias`` and ``new_alias``.

    error_msg : str
        The message of :exc:`TypeError`. It should be a string or a string
        template. If a string template defaults input ``func_name``, ``old_alias`` and
        ``new_alias``.

    **aliases : dict
        Dictionary of aliases for a function's arguments,
        like ``{old_alias: new_alias}``.

    Raises
    ------
    DeprecationWarning
        If ``old_alias`` is input into the function.

    TypeError
        If ``old_alias`` and ``new_alias`` are both input into the function.

    See Also
    --------
    dtoolkit.util._decorator.warning
    dtoolkit.util._decorator.deprecated_kwargs

    Examples
    --------
    >>> from dtoolkit.util._decorator import deprecated_alias
    >>> @deprecated_alias(a='alpha', b='beta')
    ... def plus(alpha, beta):
    ...     return alpha + beta
    >>> plus(a=1, beta=2)
    3
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for old_alias, new_alias in aliases.items():
                if old_alias in kwargs:
                    if new_alias in kwargs:
                        raise TypeError(
                            error_msg.format(
                                func_name=func.__name__,
                                old_alias=old_alias,
                                new_alias=new_alias,
                            ),
                        )

                    warn(
                        warning_msg.format(
                            func_name=func.__name__,
                            old_alias=old_alias,
                            new_alias=new_alias,
                        ),
                        DeprecationWarning,
                        find_stack_level(),
                    )

                    kwargs[new_alias] = kwargs.pop(old_alias)

            return func(*args, **kwargs)

        return wrapper

    return decorator
