import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.accessor import register_geodataframe_accessor
from dtoolkit.geoaccessor.geoseries import Tessellation as s_Tessellation


@register_geodataframe_accessor("tess")
@doc(s_Tessellation, klass="GeoDataFrame")
class Tessellation:
    def __init__(self, s: gpd.GeoSeries):
        self.tess = s_Tessellation(s.geometry)

    @doc(s_Tessellation.squares)
    def squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.squares(*args, **kwargs)

    @doc(s_Tessellation.hexagons)
    def hexagons(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.hexagons(*args, **kwargs)

    @doc(s_Tessellation.adaptive_squares)
    def adaptive_squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.adaptive_squares(*args, **kwargs)

    @doc(s_Tessellation.voronoi)
    def voronoi(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.voronoi(*args, **kwargs)

    @doc(s_Tessellation.city_blocks)
    def city_blocks(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.city_blocks(*args, **kwargs)
