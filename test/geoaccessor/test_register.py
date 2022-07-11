import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from pygeos import count_coordinates
from pygeos import from_shapely

from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geodataframe_method
@register_geoseries_method
def counts(s: gpd.GeoSeries):
    # Counts the number of coordinate pairs in geometry

    return s.geometry.apply(
        lambda x: count_coordinates(from_shapely(x)),
    )


@register_geodataframe_method
@register_geoseries_method
def counts_1(s: gpd.GeoSeries):
    # Counts the number of coordinate pairs in geometry

    return s.geometry.apply(
        lambda x: count_coordinates(from_shapely(x)),
    )


@register_geodataframe_method(name="counts_it")
@register_geoseries_method(name="counts_it")
def counts_2(s: gpd.GeoSeries):
    # Counts the number of coordinate pairs in geometry

    return s.geometry.apply(
        lambda x: count_coordinates(from_shapely(x)),
    )


s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (1 1)", None])
d = s.to_frame("geometry")


@pytest.mark.parametrize(
    "data, attr",
    [
        (s, "counts"),
        (d, "counts"),
        (s, "counts_1"),
        (d, "counts_1"),
        (s, "counts_it"),
        (d, "counts_it"),
    ],
)
def test_method_hooked_exist(data, attr):
    assert hasattr(data, attr)


@pytest.mark.parametrize(
    "data, name, expected",
    [
        (s, "counts", pd.Series([1, 1, 0])),
        (d, "counts", pd.Series([1, 1, 0], name="geometry")),
        (s, "counts_1", pd.Series([1, 1, 0])),
        (d, "counts_1", pd.Series([1, 1, 0], name="geometry")),
        (s, "counts_it", pd.Series([1, 1, 0])),
        (d, "counts_it", pd.Series([1, 1, 0], name="geometry")),
    ],
)
def test_work(data, name, expected):
    result = getattr(data, name)()

    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "data, name, attr, expected",
    [
        (s, "counts", "__name__", counts.__name__),
        (s, "counts", "__doc__", counts.__doc__),
        (d, "counts", "__name__", counts.__name__),
        (d, "counts", "__doc__", counts.__doc__),
        (s, "counts_1", "__name__", counts_1.__name__),
        (s, "counts_1", "__doc__", counts_1.__doc__),
        (d, "counts_1", "__name__", counts_1.__name__),
        (d, "counts_1", "__doc__", counts_1.__doc__),
        (s, "counts_it", "__name__", counts_2.__name__),
        (s, "counts_it", "__doc__", counts_2.__doc__),
        (d, "counts_it", "__name__", counts_2.__name__),
        (d, "counts_it", "__doc__", counts_2.__doc__),
    ],
)
def test_method_hooked_attr(data, name, attr, expected):
    method = getattr(data, name)
    result = getattr(method, attr)

    assert result == expected
