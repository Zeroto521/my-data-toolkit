import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import Point

from dtoolkit.geoaccessor.geoseries.geodistance import geodistance
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geocentroid(
    s: gpd.GeoSeries,
    /,
    weights: pd.Series = None,
    max_iter: int = 300,
    tol: float = 1e-5,
) -> Point:
    r"""
    Return the centroid of all points via the center of gravity method.

    .. math::

        \left\{\begin{matrix}
            d_i &=& D(P(\bar{x}_n, \bar{y}_n), P(x_i, y_i))  \\
            \bar{x}_0 &=& \frac{\sum w_i x_i}{\sum w_i} \\
            \bar{y}_0 &=& \frac{\sum w_i y_i}{\sum w_i} \\
            \bar{x}_{n+1} &=& \frac{\sum w_i x_i / d_i}{\sum w_i / d_i} \\
            \bar{y}_{n+1} &=& \frac{\sum w_i y_i / d_i}{\sum w_i / d_i} \\
        \end{matrix}\right.

    Parameters
    ----------
    weights : Hashable or 1d array-like, optional
        - None : All weights will be set to 1.
        - Hashable : Only for DataFrame, the column name.
        - 1d array-like : The weights of each point.

    max_iter : int, default 300
        Maximum number of iterations to perform.

    tol : float, default 1e-5
        Tolerance for convergence.

    Returns
    -------
    Point

    See Also
    --------
    geopandas.GeoSeries.centroid
    dtoolkit.geoaccessor.geoseries.geocentroid
    dtoolkit.geoaccessor.geodataframe.geocentroid

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely import Point
    >>> df = gpd.GeoDataFrame(
    ...     {
    ...         "weights": [1, 2, 3],
    ...         "geometry": [Point(100, 32), Point(120, 50), Point(122, 55)],
    ...     },
    ...     crs=4326,
    ... )
    >>> df
       weights        geometry
    0        1  POINT (100 32)
    1        2  POINT (120 50)
    2        3  POINT (122 55)
    >>> df.geocentroid()
    <POINT (120 50)>

    Set weights for each point.

    >>> df.geocentroid("weights")
    <POINT (121.999 54.999)>
    >>> df.geocentroid([1, 2, 3])
    <POINT (121.999 54.999)>
    """

    coord = s.get_coordinates()
    if len(coord) == 1:
        return Point(coord.iloc[0])

    weights = np.asarray(weights) if weights is not None else 1
    X = coord.mul(weights, axis=0).mean()

    for _ in range(max_iter):
        dis = geodistance(s, Point(X)).rdiv(1).mul(weights, axis=0)
        Xt = coord.mul(dis, axis=0).sum() / dis.sum()

        if ((X - Xt).abs() <= tol).all():
            X = Xt
            break

        X = Xt

    return Point(X)
