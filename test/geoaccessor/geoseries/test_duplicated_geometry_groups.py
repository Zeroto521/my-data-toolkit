import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from dtoolkit.geoaccessor.geodataframe import duplicated_geometry_groups  # noqa: F401


def test_warning():
    df = gpd.GeoDataFrame(
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
            Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
            Polygon([(2, 0), (3, 0), (3, 1)]),
        ],
        index=[0, 0, 1, 2],
    )

    with pytest.warns(UserWarning):
        df.duplicated_geometry_groups()
