from __future__ import annotations

from typing import Literal

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def between_replace(
    s: pd.Series,
    /,
    left,
    right,
    value,
    inclusive: Literal["both", "neither", "left", "right"] = "both",
) -> pd.Series:
    """
    Replace values in ``[left, right]`` with ``value``.

    A sugary syntax wraps the following::

        s.mask(
            s.between(
                left=left,
                right=right,
                inclusive=inclusive,
            ),
            value,
        )

    Parameters
    ----------
    left : scalar
        Left boundary.

    right : scalar
        Right boundary.

    value : scalar
        Value to replace any values range in ``[left, right]``.

    inclusive : {"both", "neither", "left", "right"}, default "both"
        Include boundaries. Whether to set each bound as closed or open.

    Returns
    -------
    Series

    See Also
    --------
    pandas.Series.between
    pandas.Series.mask

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([2, 0, 4, 8, None])
    >>> s
    0    2.0
    1    0.0
    2    4.0
    3    8.0
    4    NaN
    dtype: float64
    >>> s.between_replace(1, 4, 'here')
    0    here
    1     0.0
    2    here
    3     8.0
    4     NaN
    dtype: object

    ``left`` and ``right`` can be any scalar value.

    >>> s = pd.Series(['Alice', 'Bob', 'Carol', 'Eve'])
    >>> s
    0    Alice
    1      Bob
    2    Carol
    3      Eve
    dtype: object
    >>> s.between_replace('Anna', 'Daniel', 'here')
    0    Alice
    1     here
    2     here
    3      Eve
    dtype: object
    """

    return s.mask(
        s.between(
            left=left,
            right=right,
            inclusive=inclusive,
        ),
        value,
    )
