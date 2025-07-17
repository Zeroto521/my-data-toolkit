from __future__ import annotations

import pandas as pd

from dtoolkit._typing import Number
from dtoolkit._typing import OneDimArray
from dtoolkit.accessor.register import register_series_method


@register_series_method
def error_report(
    s: pd.Series,
    predicted: OneDimArray | list[Number],
    /,
    absolute_error: str = "absolute_error",
    relative_error: str = "relative_error",
) -> pd.DataFrame:
    """
    Calculate `absolute_error` and `relative_error` of two columns.

    .. math::

        absolute\\_error = \\lvert predicted - s \\rvert

        relative\\_error = \\frac{absolute\\_error}{s}

    Parameters
    ----------
    predicted : list of int or float, ndarrray, Series
        A array is compared to ``s``.

    columns : list of Hashable, optional
        The columns of returning DataFrame, each represents `true value`,
        `predicted value`, `absolute error`, and `relative error`.

        .. deprecated:: 0.0.19
            Please use 'absolute_error' and 'relative_error' instead.

    absolute_error : str, default 'absolute_error'
        The name of the column of absolute error.

    relative_error : str, default 'relative_error'
        The name of the column of relative error.

    Returns
    -------
    DataFrame
        Return four columns DataFrame and each represents 'true value',
        'predicted value', 'absolute error', and 'relative error'.

    Raises
    ------
    IndexError
        - If ``len(s)`` != ``len(predicted)``.
        - If ``predicted`` is Series and its index not equal to ``s``'s index.

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 3])
    >>> s.error_report([3, 2, 1])
       true  predicted  absolute_error  relative_error
    0     1          3               2        2.000000
    1     2          2               0        0.000000
    2     3          1               2        0.666667

    If the name of ``s`` or ``predicted`` is not None, the columns of
    ``error_report`` would use the name of ``s`` and ``predicted``.

    >>> s = pd.Series([1, 2, 3], name="y")
    >>> predicted = pd.Series([3, 2, 1], name="y predicted")
    >>> s.error_report(predicted)
       y  y predicted  absolute_error  relative_error
    0  1            3               2        2.000000
    1  2            2               0        0.000000
    2  3            1               2        0.666667

    Set ``absolute_error`` and ``relative_error``.

    >>> s.rename('a').error_report(
    ...     predicted.rename('b'),
    ...     absolute_error="c",
    ...     relative_error="d",
    ... )
       a  b  c         d
    0  1  3  2  2.000000
    1  2  2  0  0.000000
    2  3  1  2  0.666667
    """

    if s.size != len(predicted):
        raise IndexError(
            "Length of 'predicted' doesn't match length of 'reference'.",
        )

    if isinstance(predicted, pd.Series):
        if not s.index.equals(predicted.index):
            raise IndexError(
                "Index values of 'predicted' sequence doesn't "
                "match index values of 'reference'.",
            )
    else:
        predicted = pd.Series(predicted, index=s.index)

    absolute = (predicted - s).abs()
    relative = absolute / s
    return pd.concat(
        (
            s.rename(s.name or "true"),
            predicted.rename(predicted.name or "predicted"),
            absolute.rename(absolute_error),
            relative.rename(relative_error),
        ),
        axis=1,
    )
