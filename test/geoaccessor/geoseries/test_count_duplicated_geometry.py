import pandas as pd
import geopandas as gpd
import pytest
from pandas.testing import assert_series_equal
from shapely.geometry import Polygon

from dtoolkit.geoaccessor.geoseries import count_duplicated_geometry  # noqa: F401


@pytest.mark.parametrize(
    "s, warning",
    [
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
                    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),
                ],
                index=[0, 0],
            ),
            UserWarning,
        ),
    ],
)
def test_warning(s, warning):
    with pytest.warns(warning):
        s.count_duplicated_geometry()


@pytest.mark.parametrize(
    "s, predicate, expected",
    [
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]),
                    Polygon([(1, 1), (1, 3), (3, 3), (3, 1)]),
                ],
            ),
            "within",
            pd.Series([0, 1]),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]),
                    Polygon([(1, 1), (1, 3), (3, 3), (3, 1)]),
                ],
            ),
            "contains",
            pd.Series([1, 0]),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
                    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),
                ],
            ),
            "intersects",
            pd.Series([1, 1]),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
                    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),
                ],
            ),
            "touches",
            pd.Series([0, 0]),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
                    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),
                ],
            ),
            "crosses",
            pd.Series([0, 0]),
        ),
    ],
)
def test_work(s, predicate, expected):
    result = s.count_duplicated_geometry(predicate=predicate)

    assert_series_equal(result, expected)
