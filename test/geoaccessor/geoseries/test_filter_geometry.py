import geopandas as gpd
import pytest
from geopandas.testing import assert_geoseries_equal
from shapely.geometry import LineString, Point, Polygon, box

from dtoolkit.geoaccessor.geoseries import filter_geometry


def test_error():
    s = gpd.GeoSeries(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            LineString([(0, 0), (0, 2)]),
            LineString([(0, 0), (0, 1)]),
            Point(0, 1),
            Point(-1, -1),
        ],
    )

    with pytest.raises(ValueError):
        filter_geometry(s, box(0, 0, 2, 2), "error-predicate")


@pytest.mark.parametrize(
    "s, geometry, predicate, complement, expected",
    [
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (1, 1), (0, 1)]),
                    LineString([(0, 0), (0, 2)]),
                    LineString([(0, 0), (0, 1)]),
                    Point(0, 1),
                    Point(-1, -1),
                ],
            ),
            box(0, 0, 2, 2),
            "covered_by",
            False,
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (1, 1), (0, 1)]),
                    LineString([(0, 0), (0, 2)]),
                    LineString([(0, 0), (0, 1)]),
                    Point(0, 1),
                ],
            ),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (1, 1), (0, 1)]),
                    LineString([(0, 0), (0, 2)]),
                    LineString([(0, 0), (0, 1)]),
                    Point(0, 1),
                    Point(-1, -1),
                ],
            ),
            box(0, 0, 2, 2),
            "covered_by",
            True,
            gpd.GeoSeries([Point(-1, -1)], index=[4]),
        ),
        (
            gpd.GeoSeries(
                [
                    Polygon([(0, 0), (1, 1), (0, 1)]),
                    LineString([(0, 0), (0, 2)]),
                    LineString([(0, 0), (0, 1)]),
                    Point(0, 1),
                    Point(-1, -1),
                ],
            ),
            box(0, 0, 0, 0),
            "covered_by",
            False,
            gpd.GeoSeries(),
        ),
    ],
)
def test_work(s, geometry, predicate, complement, expected):
    result = s.filter_geometry(
        geometry=geometry,
        predicate=predicate,
        complement=complement,
    )

    assert_geoseries_equal(result, expected)
