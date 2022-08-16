import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def query(s: pd.Series, /, expr: str, **kwargs) -> pd.Series:
    """
    Query the columns of a Series with a boolean expression.

    Parameters
    ----------
    expr : str
        The query string to evaluate.

    **kwargs
        See the documentation for :meth:`pandas.eval` for complete details on
        the keyword arguments.

    Returns
    -------
    Series

    See Also
    --------
    pandas.eval
        Evaluate a Python expression as a string using various backends.

    pandas.DataFrame.query
        Evaluates a boolean expression to query DataFrame.

    dtoolkit.accessor.series.eval
        Evaluate a string describing operations on Series columns.

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
    >>> s.query("col == 1")
    a    1
    Name: col, dtype: int64
    >>> s.query("index == 'c'")
    c    3
    Name: col, dtype: int64
    """

    if not isinstance(expr, str):
        raise ValueError(
            f"'expr' must be a string to be evaluated, {type(expr)} given",
        )

    kwargs["level"] = kwargs.pop("level", 0) + 1
    kwargs["target"] = None
    mask = s.eval(expr, **kwargs)

    return s[mask]
