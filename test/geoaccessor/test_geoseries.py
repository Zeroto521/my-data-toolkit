import geopandas as gpd
import numpy as np
import pandas as pd
import pytest

from dtoolkit.geoaccessor.geoseries import geobuffer  # noqa


class TestGeoBuffer:
    def setup_method(self):
        self.s = gpd.GeoSeries.from_wkt(
            [
                "Point(120 50)",
                "Point(150 -30)",
                "Point(100 1)",
            ],
            crs="epsg:4326",
        )

    @pytest.mark.parametrize(
        "distance",
        [
            1000,
            range(3),
            [1000] * 3,
            np.asarray([1000] * 3),
            pd.Series([1000] * 3),
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

    def test_geometry_is_none(self):
        s = gpd.GeoSeries([None], crs="epsg:4326")
        b = s.geobuffer(10)

        assert b[0] is None

    def test_distance_type_is_not_num_type(self):
        with pytest.raises(TypeError):
            self.s.geobuffer(str(1))
