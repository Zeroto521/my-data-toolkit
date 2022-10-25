import pandas as pd
from pandas.core.computation.eval import eval as _eval

from dtoolkit.accessor.register import register_series_method


@register_series_method
def eval(s: pd.Series, /, expr: str, **kwargs):
    """
    Evaluate a string describing operations on Series.

    This allows ``eval`` to run arbitrary code, which can make you vulnerable to code
    injection if you pass user input to this function.

    Parameters
    ----------
    expr : str
        The expression string to evaluate.

    **kwargs
        See the documentation for :meth:`pandas.eval` for complete details on
        the keyword arguments.

    Returns
    -------
    ndarray, scalar, pandas object

    See Also
    --------
    pandas.eval
        Evaluate a Python expression as a string using various backends.

    pandas.DataFrame.eval
        Evaluate a string describing operations on DataFrame columns.

    dtoolkit.accessor.series.query
        Evaluates a boolean expression to query Series.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd

    The ``name`` should be set.

    >>> s = pd.Series([1, 2, 3], index=["a", "b", "c"], name="col")
    >>> s
    a    1
    b    2
    c    3
    Name: col, dtype: int64
    >>> s.eval("col - 1")
    a    0
    b    1
    c    2
    Name: col, dtype: int64
    >>> s.eval("d = 4")
    a    1
    b    2
    c    3
    d    4
    Name: col, dtype: int64
    >>> s.eval("col == 1")
    a     True
    b    False
    c    False
    Name: col, dtype: bool
    >>> s.eval("index == 'c'")
    a    False
    b    False
    c     True
    dtype: bool
    """

    index_resolvers = s._get_index_resolvers()
    column_resolvers = s._get_cleaned_column_resolvers()
    resolvers = column_resolvers, index_resolvers

    kwargs["level"] = kwargs.pop("level", 0) + 1
    kwargs["target"] = kwargs.get("target", s)
    kwargs["resolvers"] = tuple(kwargs.get("resolvers", ())) + resolvers

    return _eval(expr, **kwargs)
