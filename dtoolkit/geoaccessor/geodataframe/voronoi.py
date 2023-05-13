from __future__ import annotations

from typing import TYPE_CHECKING

import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.geoseries import voronoi as s_voronoi
from dtoolkit.geoaccessor.register import register_geodataframe_method

if TYPE_CHECKING:
    from shapely import MultiPolygon, Polygon


@register_geodataframe_method
@doc(s_voronoi)
def voronoi(
    df: gpd.GeoDataFrame,
    /,
    bounary: Polygon | MultiPolygon = None,
    only_edges: bool = False,
) -> gpd.GeoSeries:

    return s_voronoi(df.geometry, bounary=bounary, only_edges=only_edges)
