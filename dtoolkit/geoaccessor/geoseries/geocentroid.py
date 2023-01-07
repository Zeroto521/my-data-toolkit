import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import Point

from dtoolkit.geoaccessor.geoseries.geodistance import geodistance
from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geocentroid(
    s: gpd.GeoSeries,
    /,
    weights: pd.Series = None,
    max_iter: int = 300,
    tol: float = 1e-4,
) -> Point:
    """
    Return the centroid of all points via the center of gravity method.

    Parameters
    ----------
    weights : Hashable or 1d array-like, optional
        - None : All weights will be set to 1.
        - Hashable : Only for DataFrame, the column name.
        - 1d array-like : The weights of each point.

    max_iter : int, default 300
        Maximum number of iterations to perform.

    tol : float, default 1e-4
        Tolerance for convergence.

    Returns
    -------
    Point

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

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
       weights                    geometry
    0        1  POINT (100.00000 32.00000)
    1        2  POINT (120.00000 50.00000)
    2        3  POINT (122.00000 55.00000)
    >>> df.geocentroid()
    <POINT (112.375 44.276)>

    Set weights for each point.

    >>> df.geocentroid("weights")
    <POINT (114.516 46.675)>
    >>> df.geocentroid([1, 2, 3])
    <POINT (114.516 46.675)>
    """

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")

    weights = np.asarray(weights) if weights is not None else 1
    coord = xy(s)
    X = coord.mean()
    for _ in range(max_iter):
        dis = geodistance(s, Point(*X.tolist())).mul(weights, axis=0)
        Xt = coord.mul(dis, axis=0).sum() / dis.sum()

        if ((X - Xt).abs() <= tol).all():
            X = Xt
            break

        X = Xt

    return Point(*X.tolist())
