import geopandas as gpd
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.accessor import register_geoseries_accessor


@register_geoseries_accessor("tess")
class Tessellation:
    def __init__(self, s: gpd.GeoSeries):
        from tesspy import Tessellation as Tess

        self.tess = Tess(s.to_frame("geometry"))

    @doc()
    def squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.squares(*args, **kwargs)

    @doc()
    def hexagons(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.hexagons(*args, **kwargs)

    @doc()
    def adaptive_squares(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.adaptive_squares(*args, **kwargs)

    @doc()
    def voronoi(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.voronoi(*args, **kwargs)

    @doc()
    def city_blocks(self, *args, **kwargs) -> gpd.GeoDataFrame:
        return self.tess.city_blocks(*args, **kwargs)
