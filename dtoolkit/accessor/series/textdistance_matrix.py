from __future__ import annotations

from typing import Callable

import pandas as pd
from pandas.api.types import is_string_dtype

from dtoolkit.accessor.register import register_series_method
from dtoolkit.accessor.series.textdistance import textdistance


@register_series_method
def textdistance_matrix(
    s: pd.Series,
    /,
    other: None | pd.Series = None,
    method: Callable = None,
) -> pd.DataFrame:
    """
    Returns a ``DataFrame`` containing the text distances matrix between in ``s``
    and ``other``.

    Parameters
    ----------
    other : None or Series, default None
        If None, use ``s``.

    method : Callable, default None
        The method to calculate the distance. The first and second positional parameters
        will be compared. If None, \
`rapidfuzz.fuzz.ratio <https://maxbachmann.github.io/RapidFuzz/Usage/fuzz.html#ratio>`_.

    Returns
    -------
    DataFrame
        The values are the text distances.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'rapidfuzz'.

    TypeError
        - If ``s`` is not string dtype.
        - If ``other`` is not string dtype.

    See Also
    --------
    textdistance

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])
    >>> s
    0    hello
    1    world
    dtype: object
    >>> s.textdistance_matrix(pd.Series(["hello", "python"]))
           0          1
    0  100.0  36.363636
    1   20.0  18.181818
    """

    if other is None:
        other = s.copy()
    if not isinstance(other, pd.Series):
        raise TypeError(f"Expected Series(string), but got {type(other).__name__!r}.")
    if not is_string_dtype(other):
        raise TypeError(f"Expected Series(string), but got {other.dtype!r}.")

    return pd.concat(
        (textdistance(s, o, method=method) for o in other),
        axis=1,
        keys=other.index,
    )
