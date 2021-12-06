import geopandas as gpd
import pandas as pd
import pytest
from pyproj.crs import CRSError
from shapely.geometry import Point

from dtoolkit.geoaccessor.dataframe import points_from_xy  # noqa


class TestPointsFromXY:
    @pytest.mark.parametrize(
        "data, x, y, z, crs, drop, excepted",
        [
            # normal
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                "z",
                "EPSG:4326",
                False,
                gpd.GeoDataFrame(
                    {
                        "x": [122, 100, 0],
                        "y": [55, 1, 0],
                        "z": [0, 0, 0],
                        "geometry": [
                            Point(122, 55, 0),
                            Point(100, 1, 0),
                            Point(0, 0, 0),
                        ],
                    },
                    crs="EPSG:4326",
                ),
            ),
            # no z
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                None,
                "EPSG:4326",
                False,
                gpd.GeoDataFrame(
                    {
                        "x": [122, 100, 0],
                        "y": [55, 1, 0],
                        "z": [0, 0, 0],
                        "geometry": [
                            Point(122, 55),
                            Point(100, 1),
                            Point(0, 0),
                        ],
                    },
                    crs="EPSG:4326",
                ),
            ),
            # test crs
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                None,
                "EPSG:3857",
                False,
                gpd.GeoDataFrame(
                    {
                        "x": [122, 100, 0],
                        "y": [55, 1, 0],
                        "z": [0, 0, 0],
                        "geometry": [
                            Point(122, 55),
                            Point(100, 1),
                            Point(0, 0),
                        ],
                    },
                    crs="EPSG:3857",
                ),
            ),
            # test crs is None
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                None,
                None,
                False,
                gpd.GeoDataFrame(
                    {
                        "x": [122, 100, 0],
                        "y": [55, 1, 0],
                        "z": [0, 0, 0],
                        "geometry": [
                            Point(122, 55),
                            Point(100, 1),
                            Point(0, 0),
                        ],
                    },
                ),
            ),
            # test drop is True
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                "z",
                None,
                True,
                gpd.GeoDataFrame(
                    {
                        "geometry": [
                            Point(122, 55, 0),
                            Point(100, 1, 0),
                            Point(0, 0, 0),
                        ],
                    },
                ),
            ),
            # test drop is True
            (
                {
                    "x": [122, 100, 0],
                    "y": [55, 1, 0],
                    "z": [0, 0, 0],
                },
                "x",
                "y",
                None,
                None,
                True,
                gpd.GeoDataFrame(
                    {
                        "z": [0, 0, 0],
                        "geometry": [
                            Point(122, 55),
                            Point(100, 1),
                            Point(0, 0),
                        ],
                    },
                ),
            ),
        ],
    )
    def test_work(self, data, x, y, z, crs, drop, excepted):
        df = pd.DataFrame(data)

        result = df.points_from_xy(x, y, z, crs, drop)

        assert result.equals(excepted)

    @pytest.mark.parametrize(
        "error, x, y, z, crs",
        [
            (KeyError, "a", "y", "z", "EPSG:4326"),
            (KeyError, "x", "b", "z", "EPSG:4326"),
            (KeyError, "x", "y", "c", "EPSG:4326"),
            (CRSError, "x", "y", "z", "whatever"),
        ],
    )
    def test_error(self, error, x, y, z, crs):
        df = pd.DataFrame(
            {
                "x": [122, 100, 0],
                "y": [55, 1, 0],
                "z": [0, 0, 0],
            },
        )

        with pytest.raises(error):
            df.points_from_xy(x, y, z, crs)
