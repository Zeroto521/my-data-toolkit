import geopandas as gpd
import pytest
from geopandas.testing import assert_geoseries_equal
from shapely import LineString
from shapely import Point
from shapely import Polygon

from dtoolkit.geoaccessor.geoseries import to_h3


pytest.importorskip("h3")


@pytest.mark.parametrize(
    "s, error",
    [
        # crs != 4326
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            ValueError,
        ),
        # geometry type is not Point or Polygon
        (
            gpd.GeoSeries([LineString([(122, 55), (100, 1)])], crs=4326),
            TypeError,
        ),
    ],
)
def test_error(s, error):
    with pytest.raises(error):
        to_h3(s, 8)


@pytest.mark.parametrize(
    "s, resolution, int_dtype, expected",
    # NOTE: the `s` argument of the `GeoSeries.to_h3` could receive a GeoSeries or
    # a GeoDataFrame
    [
        # GeoSeries with Point geometries working
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            8,
            True,
            gpd.GeoSeries(
                [Point(122, 55), Point(100, 1)],
                index=[612845052823076863, 614269156845420543],
                crs=4326,
            ),
        ),
        # GeoSeries with Polygon geometries working
        (
            gpd.GeoSeries(
                [
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                ],
            ),
            4,
            True,
            gpd.GeoSeries(
                [
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((1, 0), (1, 1), (0, 1), (0, 0), (1, 0))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                    Polygon(((2, 1), (2, 2), (1, 2), (1, 1), (2, 1))),
                ],
                index=[
                    596538839648960511,
                    596538693620072447,
                    596538685030137855,
                    596538848238895103,
                    596537920525959167,
                    596538813879156735,
                    596538856828829695,
                    596538805289222143,
                    596538229763604479,
                    596537946295762943,
                    596540780974178303,
                    596540729434570751,
                    596540772384243711,
                    596538212583735295,
                    596540763794309119,
                    596537954885697535,
                    596540746614439935,
                    596538195403866111,
                    596541030082281471,
                ],
                crs=4326,
            ),
        ),
    ],
)
def test_work(s, resolution, int_dtype, expected):
    result = to_h3(s, resolution=resolution, int_dtype=int_dtype)

    assert_geoseries_equal(result, expected)
