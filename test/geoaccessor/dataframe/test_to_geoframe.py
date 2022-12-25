import geopandas as gpd
import pandas as pd
from pandas.testing import assert_frame_equal
from shapely import Point

from dtoolkit.geoaccessor.dataframe import to_geoframe  # noqa: F401


def test_original_dataframe_type():
    df = pd.DataFrame(
        pd.DataFrame(
            {
                "wkt": [
                    "POINT (1 1)",
                    "POINT (2 2)",
                    "POINT (3 3)",
                ],
            },
        )
        .from_wkt("wkt")
        .rename_geometry("geom"),
    )

    df_copy = df.copy()
    df.to_geoframe(geometry=df["geom"])

    assert_frame_equal(df, df_copy)


def test_replace_old_geoemtry():
    df = gpd.GeoDataFrame(
        {
            "label": ["a", "b"],
            "geometry": [Point(100, 1), Point(122, 50)],
        },
        crs=4326,
    ).to_geoframe(
        geometry=gpd.GeoSeries(
            [Point(0, 0), Point(1, 1)],
            crs=3857,
        ),
    )

    assert df.crs == 3857
    assert df.geometry.x.tolist() == [0, 1]
    assert df.geometry.y.tolist() == [0, 1]
