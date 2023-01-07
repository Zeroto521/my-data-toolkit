import geopandas as gpd
from shapely import Point

from dtoolkit.geoaccessor.geoseries.geodistance import geodistance
from dtoolkit.geoaccessor.geoseries.xy import xy
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geoseries_method
def geocentroid(s: gpd.GeoSeries, /, max_iter: int = 500, tol: float = 1e-5) -> Point:
    """
    Return the centroid of all points.

    Parameters
    ----------
    max_iter : int, default 500
        Maximum number of iterations to perform.

    tol : float, default 1e-5
        Tolerance for convergence.

    Returns
    -------
    Point

    Raises
    ------
    ValueError
        If the CRS is not ``ESGP:4326``.

    TypeError
        If the geometry is not a Point.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> from shapely import Point
    >>> df = gpd.GeoDataFrame(
    ...     geometry=[
    ...         Point(100, 32),
    ...         Point(120, 50),
    ...         Point(122, 55)
    ...     ],
    ...     crs=4326,
    ... )
    >>> df
                         geometry
    0  POINT (100.00000 32.00000)
    1  POINT (120.00000 50.00000)
    2  POINT (122.00000 55.00000)
    >>> df.geocentroid()
    <POINT (112.213 44.119)>
    """

    if s.crs != 4326:
        raise ValueError(f"Only support 'EPSG:4326' CRS, but got {s.crs!r}.")
    if not all(s.geom_type == "Point"):
        raise TypeError("Only support 'Point' geometry type.")

    coord = xy(s)
    X = coord.mean()
    for _ in range(max_iter):
        dis = geodistance(s, Point(*X.tolist()))
        Xt = coord.mul(dis, axis=0).sum() / dis.sum()

        if ((X - Xt).abs() <= tol).all():
            X = Xt
            break

        X = Xt

    return Point(*X.tolist())
