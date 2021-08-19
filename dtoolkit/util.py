from __future__ import annotations

from typing import Any


def multi_if_else(
    if_condition_return: list[tuple(bool, Any)],
    else_return: Any | None = None,
) -> Any | None:
    """
    Handle a series of ``if`` or ``elif``.

    Parameters
    ----------
    if_condition_return : list[tuple(bool, Any)]
        Array of tuple contains the condition and result. if the return is
        :obj:`Exception` would raise a error.
    else_return : Any or None, default is None
        The final returning result, if the result is :obj:`Exception` would
        raise an error.

    Notes
    -----
    The back of :func:`multi_if_else` is using multiple :keyword:`if` not
    one :keyword:`if` and multiple :keyword:`elif`. So :keyword:`if`'s
    condition should be more specific compare to :keyword:`elif`.

    :keyword:`elif` version:

    .. code-block:: python

        def rank(score: int) -> str:
            if not isinstance(score, int):
                raise TypeError("the 'score' must be an integer.")

            if 100 >= score >= 90:
                return 'A'
            elif score >= 70:
                return 'B'
            elif score >= 60:
                return 'C'
            elif score >= 30:
                return 'D'
            elif score >= 0:
                return 'E'
            else:
                raise ValueError(
                    "the 'score' range should be between 0 and 100.",
                )

    :keyword:`if` version:

    .. code-block:: python

        def rank(score: int) -> str:
            if not isinstance(score, int):
                raise TypeError("the 'score' must be an integer.")

            if 100 >= score >= 90:
                return 'A'
            if 90 > score >= 70:
                return 'B'
            if 70 > score >= 60:
                return 'C'
            if 60 > score >= 30:
                return 'D'
            if 30 > score >= 0:
                return 'E'

            raise ValueError("the 'score' range should be between 0 and 100.")

    Examples
    --------
    >>> from dtoolkit.util import multi_if_else
    >>> import numpy as np
    >>> array = np.asarray(
    ...     [
    ...         [1, 0],
    ...         [0, 1],
    ...     ]
    ... )
    >>> mask = array == 0
    >>> mask
    array([[False,  True],
           [ True, False]])
    >>> if_condition_return_lambda = lambda how: [
    ...     (how == "any", mask.any()),
    ...     (how == "all", mask.all()),
    ...     (how is not None, ValueError(f"Invalid how option: {how}")),
    ... ]

    >>> mask_lambda = lambda how: multi_if_else(
    ...         if_condition_return_lambda(how),
    ...         TypeError("Must specify how"),
    ...     )
    >>> mask_lambda("any")
    True
    >>> mask_lambda("all")
    False

    :func:`mask_lambda` equal to following, but with helping of
    :func:`multi_if_else` could be more easier.

    >>> def mask_lambda(how, mask):
    ...     if how == 'any':
    ...         return mask.any()
    ...     elif how == 'all':
    ...         return mask.all()
    ...     elif how is not None:
    ...         ValueError(f"Invalid how option: {how}")
    ...     else:
    ...         TypeError("Must specify how")
    """

    for condition, result in if_condition_return:
        if condition:
            if isinstance(result, Exception):
                raise result

            return result

    if isinstance(else_return, Exception):
        raise else_return

    return else_return


def wraps(wrapped):
    """
    Keep the same additional attributes with ``wrapped``.

    Can't use :meth`functools.wraps`, specially when ``wrapped`` type is
    :type:`functin` and ``wrapper`` is :type:`class`.
    """

    def decorator(wrapper):
        wrapper.__module__ = wrapped.__module__
        wrapper.__name__ = wrapped.__name__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__qualname__ = wrapped.__qualname__
        wrapper.__annotations__ = wrapped.__annotations__

        return wrapper

    return decorator
