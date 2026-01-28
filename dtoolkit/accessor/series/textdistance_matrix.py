from typing import Callable

import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def textdistance_matrix(
    s: pd.Series,
    /,
    other: None | pd.Series = None,
    method: Callable = None,
    **kwargs,
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
        will be compared. If None, :meth:`rapidfuzz.fuzz.ratio`. Recommended use methods
        in :mod:`rapidfuzz.fuzz`, and :mod:`rapidfuzz.distance`.

    **kwargs
        Additional keyword arguments passed to ``method``.

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
    rapidfuzz.fuzz
    rapidfuzz.distance
    textdistance

    Notes
    -----
    The result of comparing to None or nan value is depended on the ``method``.

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd
    >>> s = pd.Series(["hello", "world"])
    >>> s
    0    hello
    1    world
    dtype: str
    >>> s.textdistance_matrix(pd.Series(["hello", "python"]))
           0          1
    0  100.0  36.363636
    1   20.0  18.181818
    """
    from rapidfuzz.process import cdist

    if method is None:
        method = __import__("rapidfuzz").fuzz.ratio

    if other is None:
        other = s.copy()
    if not isinstance(other, pd.Series):
        raise TypeError(f"Expected Series(string), but got {type(other).__name__!r}.")

    return pd.DataFrame(
        cdist(s, other, scorer=method, workers=-1, **kwargs),
        index=s.index,
        columns=other.index,
    )
