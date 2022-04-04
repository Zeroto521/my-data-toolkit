import pandas as pd

from pandas.core.computation.eval import eval as _eval

from dtoolkit.accessor.register import register_series_method


@register_series_method
def eval(s: pd.Series, expr: str, inplace: bool = False, **kwargs):
    """
    Evaluate a string describing operations on Series.

    This allows ``eval`` to run arbitrary code, which can make you vulnerable to code
    injection if you pass user input to this function.

    Parameters
    ----------
    expr : str
        The expression string to evaluate.

    inplace : bool, default False
        If the expression contains an assignment, whether to perform the operation
        inplace and mutate the existing Series. Otherwise, a new Series is returned.

    **kwargs
        See the documentation for :meth:`pandas.eval` for complete details on
        the keyword arguments.

    Returns
    -------
    ndarray, scalar, pandas object, or None
        The result of the evaluation or None if ``inplace=True``.

    See Also
    --------
    query
        Evaluates a boolean expression to query Series.
    pandas.eval
        Evaluate a Python expression as a string using various backends.
    """
    inplace = validate_bool_kwarg(inplace, "inplace")

    index_resolvers = s._get_index_resolvers()
    column_resolvers = s._get_cleaned_column_resolvers()
    resolvers = column_resolvers, index_resolvers

    return _eval(
        expr,
        inplace=inplace,
        **{
            **kwargs,
            "level": kwargs.pop("level", 0) + 1,
            "target": kwargs.get("target", s),
            "resolvers": tuple(kwargs.get("resolvers", ())) + resolvers,
        },
    )
