import geopandas as gpd
import pytest
from shapely import Point

from dtoolkit.geoaccessor.geoseries import geoazimuth


@pytest.mark.parametrize(
    "s, other, align, error",
    [
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            True,
            ValueError,
        ),
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            None,
            True,
            TypeError,
        ),
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            True,
            ValueError,
        ),
        (
            gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326),
            gpd.GeoSeries([Point(122, 55), Point(100, 1)]),
            True,
            ValueError,
        ),
    ],
)
def test_error(s, other, align, error):
    with pytest.raises(error):
        geoazimuth(s, other, align=align)


def test_warning():
    s1 = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)
    s2 = gpd.GeoSeries([Point(120, 30), Point(120, 50)], index=[1, 2], crs=4326)

    with pytest.warns(UserWarning):
        geoazimuth(s1, s2)


def test_point():
    s = gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326)

    result = s.geoazimuth(Point(120, 30))
    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(227.47864507273914)


def test_aligned_pair():
    s1 = gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326)
    s2 = gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326)

    result = s1.geoazimuth(s2)
    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(316.5025060397356)


def test_unaligned_pair():
    s1 = gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326)
    s2 = gpd.GeoSeries([Point(120, 30), Point(110, 40)], index=[0, 1], crs=4326)

    result = s1.geoazimuth(s2, align=False)

    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(316.5025060397356)


def test_range():
    s = gpd.GeoSeries(
        [Point(0, 0), Point(90, 0), Point(0, 90)],
        crs=4326,
    )
    target = gpd.GeoSeries([Point(1, 0)] * 3, crs=4326)

    result = s.geoazimuth(target)

    assert result.iloc[0] == pytest.approx(90.0)
    assert result.iloc[1] == pytest.approx(270.0)
    assert 0 <= result.iloc[2] < 360


def test_geodataframe():
    s = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326)
    df = gpd.GeoSeries([Point(122, 55), Point(100, 1)], crs=4326).to_frame("geometry")

    assert isinstance(df, gpd.GeoDataFrame)
    result = s.geoazimuth(df)

    assert all(result == 0)
