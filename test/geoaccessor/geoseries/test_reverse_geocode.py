import geopandas as gpd
import pytest

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
