from __future__ import annotations

from typing import Any


def multi_if_else(
    if_condition_return: list[tuple(bool, Any)],
    else_return: Any | None = None,
    if_condition_raise: list[tuple(bool, Any)] | None = None,
    else_raise: Any | None = None,
) -> Any | None:
    """
    Handle a series of ``if``, ``elif`` and ``else``.

    Parameters
    ----------
    if_condition_return : list[tuple(bool, Any)]
        Array of tuple contains the condition and result.
    else_return : Any or None, default is None
        The final returning result.
    if_condition_raise: list[tuple(bool, Any)] or None, default is None
        Array of tuple contains the condition and error.
    else_raise : Any or None, default is None
        The final raise error, if the value is None, nothing would be raised.

    Examples
    --------
    >>> from dtoolkit._util import multi_if_else
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
    ... ]
    >>> if_condition_raise_lambda = lambda how: [
    ...     (how is not None, ValueError(f"Invalid how option: {how}")),
    ... ]
    >>> mask_lambda = lambda how: multi_if_else(
    ...         if_condition_return=if_condition_return_lambda(how),
    ...         if_condition_raise=if_condition_raise_lambda(how),
    ...         else_raise=TypeError("Must specify how"),
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
            return result

    if if_condition_raise:
        for condition, error in if_condition_raise:
            if condition:
                raise error

    if else_raise:
        raise else_raise

    return else_return
