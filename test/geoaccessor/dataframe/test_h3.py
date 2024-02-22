import geopandas as gpd
import pytest
from shapely import Point

from dtoolkit.geoaccessor.series import H3  # noqa: F401


pytest.importorskip("h3")


# -----------------------------------------------------------------------
# test dataframe h3 accessor compat with geodataframe
# -----------------------------------------------------------------------


@pytest.mark.parametrize(
    "df, klass, crs",
    [
        # test to_str
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8)
                .h3.to_str()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_int
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_int()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_center_child
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_center_child()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_center_child
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_center_child()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_children
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_children()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_parent
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_parent()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_points
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_points()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
        # test to_polygons
        (
            (
                gpd.GeoDataFrame(
                    {
                        "label": ["a", "b"],
                        "geometry": [Point(100, 1), Point(122, 55)],
                    },
                    crs=4326,
                )
                .to_h3(8, int_dtype=False)
                .h3.to_polygons()
            ),
            gpd.GeoDataFrame,
            4326,
        ),
    ],
)
def test_geodataframe_h3_accessor_return(df, klass, crs):
    # test return type
    assert isinstance(df, klass)

    # test crs
    if isinstance(df, gpd.GeoDataFrame):
        assert df.crs == crs
