import geopandas as gpd
import pytest
from geopandas.testing import assert_geodataframe_equal

from dtoolkit.geoaccessor.geoseries import reverse_geocode


pytest.importorskip("geopy")


@pytest.mark.parametrize(
    "s, error",
    [
        (gpd.GeoSeries.from_wkt(["POINT (0 0)"]), ValueError),
        (gpd.GeoSeries.from_wkt(["POINT (0 0)"], crs=3857), ValueError),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        reverse_geocode(s)


def test_work():
    s = gpd.GeoSeries.from_wkt(["POINT (-90 0)", "POINT (-180 -90)"], crs=4326)
    expected = gpd.GeoDataFrame({"address": [None, "South Pole"], "geometry": s})

    assert_geodataframe_equal(s.reverse_geocode(), expected)
