from typing import TYPE_CHECKING

import geopandas as gpd
from shapely import voronoi_polygons

from dtoolkit.geoaccessor.register import register_geoseries_method

if TYPE_CHECKING:
    from shapely import MultiPolygon
    from shapely import Polygon


@register_geoseries_method
def voronoi(
    s,
    /,
    boundary: Polygon | MultiPolygon = None,
    only_edges: bool = False,
) -> gpd.GeoSeries:
    """
    Computes a Voronoi diagram from Point geometry.

    Parameters
    ----------
    boundary : Polygon or MultiPolygon, optional
        The outer boundary of the diagram. If None, use the convex hull of the inputs.

    only_edges : bool, default False
        If True, only return the edges.

    Returns
    -------
    GeoSeries

    Raises
    ------
    TypeError
        If the geometry type is not Point.

    IndexError
        If the length of the GeoSeries is less than 3.

    See Also
    --------
    dtoolkit.geoaccessor.geoseries.voronoi
    dtoolkit.geoaccessor.geodataframe.voronoi

    Notes
    -----
    These Points may construct a polygon.

    Examples
    --------
    >>> import dtoolkit.geoaccessor
    >>> import geopandas as gpd
    >>> df = gpd.GeoDataFrame(geometry=gpd.points_from_xy([0, 1, 2], [0, 1, 0]))
    >>> df
          geometry
    0  POINT (0 0)
    1  POINT (1 1)
    2  POINT (2 0)
    >>> df.voronoi()
    0             POLYGON ((1 0, 0 0, 0.5 0.5, 1 0))
    2         POLYGON ((1.5 0.5, 2 0, 1 0, 1.5 0.5))
    1    POLYGON ((1 0, 0.5 0.5, 1 1, 1.5 0.5, 1 0))
    dtype: geometry
    """

    if all(s.geom_type != "Point"):
        raise TypeError("Only support 'Point' geometry type.")
    elif len(s) < 3:
        raise IndexError(f"{len(s)=} < 3.")

    return gpd.GeoSeries(
        list(
            voronoi_polygons(
                s.unary_union,
                only_edges=only_edges,
            ).geoms,
        ),
        crs=s.crs,
    ).clip(boundary or s.unary_union.convex_hull)
