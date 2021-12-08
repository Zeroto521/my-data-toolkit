from __future__ import annotations

import geopandas as gpd
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def points_from_xy(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str | None = None,
    crs: str | None = None,
    drop: bool = False,
):
    """
    Generate :obj:`~geopandas.GeoDataFrame` of :obj:`~shapely.geometry.Point`
    geometries from columns of :obj:`~pandas.DataFrame`.

    Parameters
    ----------
    x: str
        ``df``'s column name.
    y: str
        ``df``'s column name.
    z: str, optional
        ``df``'s column name.
    crs: str, optional
        Coordinate Reference System of the geometry objects. Can be anything
        accepted by :meth:`~pyproj.crs.CRS.from_user_input`, such as an authority
        string (eg "EPSG:4326") or a WKT string.
    drop: bool, default False
        Don't contain ``x``, ``y`` and ``z`` anymore.

    Returns
    -------
    GeoDataFrame

    See Also
    --------
    geopandas.points_from_xy
    geopandas.GeoSeries.from_xy

    Notes
    -----
    This method is the accessor of DataFrame, not GeoDataFrame.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({"x": [122, 100], "y":[55, 1]})
    >>> df
         x   y
    0  122  55
    1  100   1
    >>> df.points_from_xy("x", "y", crs="EPSG:4326")
         x   y                    geometry
    0  122  55  POINT (122.00000 55.00000)
    1  100   1   POINT (100.00000 1.00000)

    Drop original 'x' and 'y'.

    >>> df.points_from_xy("x", "y", drop=True)
                         geometry
    0  POINT (122.00000 55.00000)
    1   POINT (100.00000 1.00000)
    """

    result = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(
            df[x],
            df[y],
            z=df[z] if z is not None else z,
            crs=crs,
        ),
    )

    if drop:
        result.drop(
            columns=[x, y, z] if z is not None else [x, y],
            inplace=True,
        )

    return result
