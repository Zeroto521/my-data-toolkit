import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from pyproj import CRS

from dtoolkit.geoaccessor.geoseries import geobuffer  # noqa


my_wkts = ["Point(120 50)", "Point(150 -30)", "Point(100 1)"]
distances = np.asarray(range(1, 1000, 499))


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
