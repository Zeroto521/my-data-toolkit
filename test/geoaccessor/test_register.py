import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dtoolkit.geoaccessor.register import register_geodataframe_method
from dtoolkit.geoaccessor.register import register_geoseries_method


@register_geodataframe_method
@register_geoseries_method
def is_point(s: gpd.GeoSeries | gpd.GeoDataFrame) -> pd.Series:
    """
    Return a boolean Series denoting whether each geometry is a point.

    Parameters
    ----------
    s : GeoSeries or GeoDataFrame

    Returns
    -------
    Series
    """

    return s.geometry.geom_type == "Point"


@register_geodataframe_method("is_point_another")
@register_geoseries_method("is_point_another")
def is_point_2(s: gpd.GeoSeries):
    # Return a boolean Series denoting whether each geometry is a point.

    return is_point(s)


s = gpd.GeoSeries.from_wkt(["POINT (0 0)", "POINT (1 1)", None])
d = s.to_frame("geometry")


@pytest.mark.parametrize(
    "data, attr",
    [
        (s, "is_point"),
        (d, "is_point"),
        (s, "is_point_another"),
        (d, "is_point_another"),
    ],
)
def test_method_hooked_exist(data, attr):
    assert hasattr(data, attr)


@pytest.mark.parametrize(
    "data, name, expected",
    [
        (s, "is_point", pd.Series([True, True, False])),
        (d, "is_point", pd.Series([True, True, False])),
        (s, "is_point_another", pd.Series([True, True, False])),
        (d, "is_point_another", pd.Series([True, True, False])),
    ],
)
def test_work(data, name, expected):
    result = getattr(data, name)()

    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "data, name, attr, expected",
    [
        (s, "is_point", "__name__", is_point.__name__),
        (s, "is_point", "__doc__", is_point.__doc__),
        (d, "is_point", "__name__", is_point.__name__),
        (d, "is_point", "__doc__", is_point.__doc__),
        (s, "is_point_another", "__name__", is_point_2.__name__),
        (s, "is_point_another", "__doc__", is_point_2.__doc__),
        (d, "is_point_another", "__name__", is_point_2.__name__),
        (d, "is_point_another", "__doc__", is_point_2.__doc__),
    ],
)
def test_method_hooked_attr(data, name, attr, expected):
    method = getattr(data, name)
    result = getattr(method, attr)

    assert result == expected
