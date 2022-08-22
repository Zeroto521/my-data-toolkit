import pytest

gpd = pytest.importorskip("geopandas")

import numpy as np
import pandas as pd
from pyproj import CRS

from dtoolkit.geoaccessor.geodataframe import geobuffer  # noqa: F401


my_wkts = ["Point(120 50)", "Point(150 -30)", "Point(100 1)"]
distances = np.asarray(range(1, 1000, 499))


df = gpd.GeoSeries.from_wkt(my_wkts, crs="epsg:4326").to_frame("geometry")
crs = CRS.from_user_input("epsg:4326")


@pytest.mark.parametrize(
    "distance",
    [
        1000,
        list(distances),
        distances,
        pd.Series(distances),
    ],
)
def test_distance_work(distance):
    b = df.geobuffer(distance)

    assert isinstance(b, gpd.GeoDataFrame)


def test_distance_index_is_different_to_data():
    df_distance = pd.Series(range(1, 1000, 499), index=["a", "b", "c"])
    with pytest.raises(IndexError):
        df.geobuffer(df_distance)


def test_distance_length_is_different_to_data():
    with pytest.raises(IndexError):
        df.geobuffer([1, 1000])


def test_renamed_geometry():
    default_geometry_column_name = "geometry"
    new_geometry_column_name = "geom"

    df_renamed = df.rename_geometry(new_geometry_column_name)
    result = df_renamed.geobuffer(10)

    assert new_geometry_column_name in result.columns
    assert default_geometry_column_name not in result.columns
