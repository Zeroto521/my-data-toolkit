from __future__ import annotations

from typing import Hashable
from typing import Literal
from typing import TYPE_CHECKING

import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from sklearn.base import RegressorMixin


@register_dataframe_method
def fillna_regression(
    df: pd.DataFrame,
    /,
    method: RegressorMixin,
    columns: dict[Hashable, Hashable | list[Hashable] | pd.Index],
    how: Literal["na", "all"] = "na",
    **kwargs,
) -> pd.DataFrame:
    """
    Fill na value with regression algorithm.

    Parameters
    ----------
    method : RegressorMixin
        Regression transformer.

    columns : dict, ``{y: X}``
        A series of column names pairs. The key is the y (or target) column name, and
        values are X (or feature) column names.

    how : {'na', 'all'}, default 'na'
        Only fill na value or apply regression to entire target column.

    **kwargs
        See the documentation for ``method`` for complete details on
        the keyword arguments.

    Returns
    -------
    DataFrame

    Raises
    ------
    ValueError
        If ``how`` isn't "na" or "all".

    See Also
    --------
    sklearn.kernel_ridge
    sklearn.linear_model
    sklearn.dummy.DummyRegressor
    sklearn.ensemble.AdaBoostRegressor
    sklearn.ensemble.BaggingRegressor
    sklearn.ensemble.ExtraTreesRegressor
    sklearn.ensemble.GradientBoostingRegressor
    sklearn.ensemble.RandomForestRegressor
    sklearn.ensemble.StackingRegressor
    sklearn.ensemble.VotingRegressor
    sklearn.ensemble.HistGradientBoostingRegressor
    sklearn.gaussian_process.GaussianProcessRegressor
    sklearn.isotonic.IsotonicRegression
    sklearn.kernel_ridge.KernelRidge
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

    >>> df.fillna_regression(LinearRegression, {'y': ['x1', 'x2']})
       x1  x2     y
    0   1   1   6.0
    1   1   2   8.0
    2   2   2   9.0
    3   2   3  11.0
    4   3   5  16.0
    """

    if how not in {"na", "all"}:
        raise ValueError(f"invalid inf option: {how!r}")

    df = df.copy()  # avoid mutating the original dataframe
    for y, X in columns.items():
        df = _fillna_regression(df, method, y, X, how=how, **kwargs)

    return df


def _fillna_regression(
    df: pd.DataFrame,
    /,
    method: RegressorMixin,
    y: Hashable,
    X: Hashable | list[Hashable] | pd.Index,
    how: Literal["na", "all"],
    **kwargs,
):
    """Fill single na column at once."""

    if isinstance(X, (str, int)):
        X = [X]

    data = df[df[y].notnull()]
    model = method(**kwargs).fit(data[X], data[y])

    if how == "all":
        df[y] = model.predict(df[X])
    elif how == "na":
        index_null = df[y].isnull()
        df.loc[index_null, y] = model.predict(df.loc[index_null, X])

    return df
