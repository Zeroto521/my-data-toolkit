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
        The final returning result, if the result is :obj:``Exception`` would
        raise an error.

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

    if isinstance(result, Exception):
        raise else_return

    return else_return
