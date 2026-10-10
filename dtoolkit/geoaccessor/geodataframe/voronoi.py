from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd

from dtoolkit.geoaccessor.geoseries import voronoi as s_voronoi
from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.util._decorator import doc

if TYPE_CHECKING:
    from shapely import MultiPolygon, Polygon


@register_geodataframe_method
@doc(s_voronoi)
def voronoi(
    df: gpd.GeoDataFrame,
    /,
    boundary: Polygon | MultiPolygon = None,
    only_edges: bool = False,
) -> gpd.GeoSeries:
    return s_voronoi(df.geometry, boundary=boundary, only_edges=only_edges)
