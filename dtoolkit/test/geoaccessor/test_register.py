import geopandas as gpd
import pandas as pd
from pygeos import count_coordinates
from pygeos import from_shapely

from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geodataframe_method
@register_geoseries_method
def counts(s: gpd.GeoSeries):
    # Counts the number of coordinate pairs in geometry

    return s.geometry.apply(
        lambda x: count_coordinates(from_shapely(x)),
    )


s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (1 1)", None])
d = gpd.GeoDataFrame(geometry=s)


def test_method_hooked():
    assert hasattr(s, "counts")
    assert hasattr(d, "counts")


def test_work():
    result = pd.Series([1, 1, 0], name="geometry")
    assert s.counts().equals(result)
    assert d.counts().equals(result)
