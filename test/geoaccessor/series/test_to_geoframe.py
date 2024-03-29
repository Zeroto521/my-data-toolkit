import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from geopandas.testing import assert_geodataframe_equal
from shapely import Point

from dtoolkit.geoaccessor.series import to_geoframe  # noqa: F401


@pytest.mark.parametrize(
    "s, geometry, expected",
    [
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry,
            ),
            None,
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry,
            ),
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry
            ),
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            (
                pd.Series(
                    [
                        "POINT (1 1)",
                        "POINT (2 2)",
                        "POINT (3 3)",
                    ],
                    name="wkt",
                )
                .from_wkt()
                .geometry
            ),
            gpd.GeoDataFrame,
        ),
        (
            pd.Series(
                [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            ),
            None,
            pd.DataFrame,
        ),
    ],
)
def test_type(s, geometry, expected):
    result = s.to_geoframe(geometry=geometry)

    assert isinstance(s, pd.Series)
    assert isinstance(result, expected)


# https://github.com/geopandas/geopandas/issues/2660
@pytest.mark.parametrize(
    "s, geometry, expected",
    [
        # geometry is a list of shapely geometry objects
        (
            pd.Series([1, 2], name="name", index=[1, 2]),
            [Point(1, 1), Point(2, 2)],
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [Point(1, 1), Point(2, 2)],
                },
                index=[1, 2],
            ),
        ),
        # geometry is a array of shapely geometry objects
        (
            pd.Series([1, 2], name="name", index=[1, 2]),
            np.asarray([Point(1, 1), Point(2, 2)]),
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [Point(1, 1), Point(2, 2)],
                },
                index=[1, 2],
            ),
        ),
        # s's index is same to geometry's index
        (
            pd.Series([1, 2], name="name", index=[1, 2]),
            gpd.GeoSeries([Point(1, 1), Point(2, 2)], index=[1, 2]),
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [Point(1, 1), Point(2, 2)],
                },
                index=[1, 2],
            ),
        ),
        # s's index is partly different from geometry's index
        (
            pd.Series([1, 2], name="name", index=[0, 1]),
            gpd.GeoSeries([Point(1, 1), Point(2, 2)], index=[1, 2]),
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [Point(1, 1), Point(2, 2)],
                },
                index=[0, 1],
            ),
        ),
        # s's index is totally different from geometry's index
        (
            pd.Series([1, 2], name="name", index=[0, 1]),
            gpd.GeoSeries([Point(1, 1), Point(2, 2)], index=[2, 3]),
            gpd.GeoDataFrame(
                {
                    "name": [1, 2],
                    "geometry": [Point(1, 1), Point(2, 2)],
                },
                index=[0, 1],
            ),
        ),
    ],
)
def test_index(s, geometry, expected):
    result = to_geoframe(s, geometry=geometry)

    assert_geodataframe_equal(result, expected)


# https://github.com/Zeroto521/my-data-toolkit/issues/815
def test_crs():
    result = to_geoframe(
        pd.Series([1, 2]),
        geometry=gpd.GeoSeries(
            [
                Point(1, 1),
                Point(2, 2),
            ],
            crs=4326,
        ),
    )

    assert result.crs == 4326
