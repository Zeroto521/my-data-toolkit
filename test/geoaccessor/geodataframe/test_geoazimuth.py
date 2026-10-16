import geopandas as gpd
import pytest
from shapely import Point


def test_geodataframe_point():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )

    result = df.geoazimuth(Point(120, 30))

    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(227.47864507273914)


def test_geodataframe_series():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )
    s = gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326)

    result = df.geoazimuth(s)

    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(316.5025060397356)


def test_geodataframe_geodataframe():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )
    other = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(120, 30), Point(110, 40)], crs=4326),
    )

    result = df.geoazimuth(other)

    assert result[0] == pytest.approx(162.34309829667646)
    assert result[1] == pytest.approx(316.5025060397356)


def test_geodataframe_error_crs():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9)], crs=4326),
    )
    with pytest.raises(ValueError):
        df.geoazimuth(gpd.GeoSeries([Point(120, 30)]))


def test_geodataframe_error_type():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9)], crs=4326),
    )
    with pytest.raises(TypeError):
        df.geoazimuth("string")


def test_self_azimuth_zero():
    df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([Point(116.4, 39.9), Point(121.5, 31.2)], crs=4326),
    )

    result = df.geoazimuth(df.geometry)

    assert (result == 0).all()
