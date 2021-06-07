import geopandas as gpd
import pandas._testing as tm
from dtoolkit.buffer import geographic_buffer


my_wkts = ["Point(120 50)", "Point(150 -30)", "Point(100 1)"]


def test_type():
    s = gpd.GeoSeries.from_wkt(my_wkts, crs="epsg:4326")
    buffers = geographic_buffer(s, 1000)

    assert all(buffers.type == "Polygon")


def test_missing_crs():
    with tm.assert_produces_warning(UserWarning) as w:
        s = gpd.GeoSeries.from_wkt(my_wkts)
        geographic_buffer(s, 1000)

    msg = str(w[0].message)
    assert "EPSG:4326" in msg
    assert "missing" in msg
