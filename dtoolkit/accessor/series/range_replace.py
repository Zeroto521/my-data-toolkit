from __future__ import annotations

from typing import Literal

import pandas as pd
from pandas.api.types import is_dict_like
from pandas.api.types import is_list_like

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.between_replace import between_replace


@register_series_method
def range_replace(
    s: pd.Series,
    /,
    to_replace: dict,
    inclusive: Literal["both", "neither", "left", "right"] = "both",
    limit: int = None,
    regex: bool = False,
    method: Literal["pad", "ffill", "bfill"] = None,
) -> pd.Series:
    """
    Replace values in ``[left, right]`` with ``value``.

    Parameters
    ----------
    to_replace : dict
        - ``{(left, right): value}``
            Find the values in ``[left, right]`` and will be replaced via ``value``.
        - ``{key: value}``
        - ``{keys: value}``

    inclusive : {"both", "neither", "left", "right"}, default "both"
        Include boundaries. Whether to set each bound as closed or open.

    limit, regex, method
        Works when one of ``to_replace`` elements isn't ``{(left, right): value}``.
        See the documentation for :meth:`pandas.Series.replace` for complete details on
        the keyword arguments.

    Returns
    -------
    Series

    Raises
    ------
    TypeError
        If ``to_replace`` is not a :obj:`dict`.

    See Also
    --------
    pandas.Series.replace
    dtoolkit.accessor.series.bin
    dtoolkit.accessor.series.between_replace

    Notes
    -----
    - Different from :func:`~dtoolkit.accessor.series.bin`.
        - :func:`~dtoolkit.accessor.series.range_replace` supports scalar type and could
         replace a part of values.
        - :func:`~dtoolkit.accessor.series.bin` is used to replace all values and only
         works for number type.
    - Different from :func:`pandas.Series.replace`.
        This method is a patch to :func:`pandas.Series.replace` and supports replacing
        a range of values.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> s = pd.Series([93, 99, 100, 63, 46, 78, 87])
    >>> s
    0     93
    1     99
    2    100
    3     63
    4     46
    5     78
    6     87
    dtype: int64
    >>> s.replace({100: "S", (93, 99): "A", (78, 87): "B", 63: "C", 46: "D"})
    0    A
    1    A
    2    S
    3    C
    4    D
    5    B
    6    B
    dtype: object

    Simplify a bit via ``range_replace``.

    >>> s.range_replace(
    ...     {
    ...         100: "S",
    ...         (90, 99): "A",
    ...         (70, 89): "B",
    ...         (60, 79): "C",
    ...         (0, 59): "D",
    ...     }
    ... )
    0    A
    1    A
    2    S
    3    C
    4    D
    5    B
    6    B
    dtype: object
    """

    if not is_dict_like(to_replace):
        raise TypeError(
            "Expecting 'to_replace' to be a dict, got invalid type "
            f"{type(to_replace).__name__!r}",
        )

    for key, value in to_replace.items():
        if is_list_like(key) and len(key) == 2 and key[0] < key[1]:
            s = between_replace(s, *key, value, inclusive=inclusive)
        else:
            s = s.replace(key, value, limit=limit, regex=regex, method=method)

    return s
