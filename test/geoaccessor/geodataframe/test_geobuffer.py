import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from pyproj import CRS

from dtoolkit.geoaccessor.geodataframe import geobuffer  # noqa: F401


df = gpd.GeoSeries.from_wkt(
    [
        "Point(120 50)",
        "Point(150 -30)",
        "Point(100 1)",
    ],
    crs="epsg:4326",
).to_frame("geometry")


@pytest.mark.parametrize(
    "distance",
    [
        1000,
        list(range(1, 1000, 499)),
        np.asarray(range(1, 1000, 499)),
        pd.Series(range(1, 1000, 499)),
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
