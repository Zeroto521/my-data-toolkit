import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from pyproj import CRS
from shapely import wkt
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.geoseries import _geographic_buffer
from dtoolkit.geoaccessor.geoseries import geobuffer  # noqa


my_wkts = ["Point(120 50)", "Point(150 -30)", "Point(100 1)"]
my_points = [wkt.loads(i) for i in my_wkts]
distances = np.asarray(range(1, 1000, 499))


#
# _geographic_buffer tests
#


class TestGeographicBuffer:
    def setup_method(self):
        self.p = my_points[0]
        self.crs = CRS.from_user_input("epsg:4326")
        self.distance = 1000

    @pytest.mark.parametrize("geom", my_points)
    @pytest.mark.parametrize("distance", distances)
    def test_work(self, geom, distance):
        b = _geographic_buffer(geom, distance, self.crs)
        assert isinstance(b, BaseGeometry)

    def test_geometry_is_none(self):
        res = _geographic_buffer(None, self.distance, self.crs)
        assert res is None

    def test_distance_type_is_not_num_type(self):
        with pytest.raises(TypeError):
            _geographic_buffer(self.p, str(self.distance), self.crs)

    @pytest.mark.parametrize("distance", [0, -1000])
    def test_distance_less_then_zero(self, distance):
        with pytest.raises(ValueError):
            _geographic_buffer(self.p, distance, crs=self.crs)


class TestGeoBuffer:
    def setup_method(self):
        self.s = gpd.GeoSeries.from_wkt(my_wkts, crs="epsg:4326")
        self.crs = CRS.from_user_input("epsg:4326")

    @pytest.mark.parametrize(
        "distance",
        [
            1000,
            list(distances),
            distances,
            pd.Series(distances),
        ],
    )
    def test_distance_work(self, distance):
        b = self.s.geobuffer(distance)
        assert isinstance(b, gpd.GeoSeries)

    def test_distance_is_pd_series(self):
        df_distance = pd.Series(range(1, 1000, 499))
        self.s.geobuffer(df_distance)

    def test_distance_index_is_different_to_data(self):
        df_distance = pd.Series(range(1, 1000, 499), index=["a", "b", "c"])
        with pytest.raises(IndexError):
            self.s.geobuffer(df_distance)

    def test_distance_length_is_different_to_data(self):
        with pytest.raises(IndexError):
            self.s.geobuffer([1, 1000])
