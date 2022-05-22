from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit._typing import IntOrStr
from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from sklearn.base import RegressorMixin


@register_dataframe_method
def fillna_regression(
    df: pd.DataFrame,
    method: RegressorMixin,
    X: IntOrStr | list[IntOrStr] | pd.Index,
    y: IntOrStr,
    how: str = "na",
    **kwargs,
) -> pd.DataFrame:
    """
    Fill na value with regression algorithm.

    Parameters
    ----------
    method : RegressorMixin
        Regression transformer.

    X : int or str, list of int or str, Index
        Feature columns.

    y : int or str
        Target column.

    how : {'na', 'all'}, default 'na'
        Only fill na value or apply regression to entire target column.

    **kwargs
        See the documentation for ``method`` for complete details on
        the keyword arguments.

    See Also
    --------
    sklearn.kernel_ridge
    sklearn.linear_model
    sklearn.neighbors.KNeighborsRegressor
    sklearn.neighbors.RadiusNeighborsRegressor
    sklearn.neural_network.MLPRegressor
    sklearn.svm.LinearSVR
    sklearn.svm.NuSVR
    sklearn.svm.SVR
    sklearn.tree.DecisionTreeRegressor
    sklearn.tree.ExtraTreeRegressor

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> from sklearn.linear_model import LinearRegression

    .. math:: y = 1 \\times x_0 + 2 \\times x_1 + 3

    >>> df = pd.DataFrame(
    ...     [
    ...         [1, 1, 6],
    ...         [1, 2, 8],
    ...         [2, 2, 9],
    ...         [2, 3, 11],
    ...         [3, 5, None],
    ...     ],
    ...     columns=['x1', 'x2', 'y'],
    ... )
    >>> df
       x1  x2     y
    0   1   1   6.0
    1   1   2   8.0
    2   2   2   9.0
    3   2   3  11.0
    4   3   5   NaN

    Use 'x1' and 'x2' columns to fit 'y' column and fill the value.

    >>> df.fillna_regression(LinearRegression, ['x1', 'x2'], 'y')
       x1  x2     y
    0   1   1   6.0
    1   1   2   8.0
    2   2   2   9.0
    3   2   3  11.0
    4   3   5  16.0
    """

    if how not in {"na", "all"}:
        raise ValueError(f"invalid inf option: {how!r}")

    if isinstance(X, (str, int)):
        X = [X]

    index_notnull = df[df[y].notnull()].index
    model = method(**kwargs).fit(
        df.loc[index_notnull, X],
        df.loc[index_notnull, y],
    )

    if how == "all":
        df[y] = model.predict(df[X])
    elif how == "na":
        index_null = df[df[y].isnull()].index
        df.loc[index_null, y] = model.predict(df.loc[index_null, X])

    return df
