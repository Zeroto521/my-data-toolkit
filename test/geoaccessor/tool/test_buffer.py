import numpy as np
import pytest
from pyproj import CRS
from shapely import wkt
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from dtoolkit.geoaccessor.tool import geographic_buffer


my_wkts = ["Point(120 50)", "Point(150 -30)", "Point(100 1)"]
my_points = [wkt.loads(i) for i in my_wkts]
distances = np.asarray(range(1, 1000, 499))


class TestGeographicBuffer:
    def setup_method(self):
        self.p = my_points[0]
        self.crs = CRS.from_user_input("epsg:4326")
        self.distance = 1000

    @pytest.mark.parametrize("geom", my_points)
    @pytest.mark.parametrize("distance", distances)
    def test_work(self, geom, distance):
        b = geographic_buffer(geom, distance, self.crs)
        assert isinstance(b, BaseGeometry)

    def test_geometry_is_none(self):
        result = geographic_buffer(None, self.distance, self.crs)
        assert result is None

    def test_geometry_is_not_geometry(self):
        with pytest.raises(TypeError):
            geographic_buffer(1, self.distance, self.crs)

    def test_geometry_is_not_point(self):
        polygon = Polygon([(0, 0), (1, 1), (1, 0)])
        result = geographic_buffer(polygon, self.distance, self.crs)
        assert result is polygon

    def test_distance_type_is_not_num_type(self):
        with pytest.raises(TypeError):
            geographic_buffer(self.p, str(self.distance), self.crs)

    @pytest.mark.parametrize("distance", [0, -1000])
    def test_distance_less_then_zero(self, distance):
        with pytest.raises(ValueError):
            geographic_buffer(self.p, distance, crs=self.crs)
