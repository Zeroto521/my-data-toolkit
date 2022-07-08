import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.geoaccessor.geodataframe import drop_geometry  # noqa


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy("x", "y"),
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}),
        ),
        # test non default geometry name
        (
            (
                pd.DataFrame({"x": [122, 100], "y": [55, 1]})
                .from_xy("x", "y")
                .rename_geometry("geom")
            ),
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}),
        ),
        (
            (
                pd.DataFrame({"x": [122, 100], "y": [55, 1]})
                .from_xy("x", "y")
                .rename_geometry(0)
            ),
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}),
        ),
        # test single column dataframe
        (
            (
                pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy(
                    "x", "y", drop=True
                )
            ),
            pd.DataFrame(index=[0, 1]),
        ),
    ],
)
def test_work(df, expected):
    result = df.drop_geometry()

    # The return of `.drop(columns='geometry')` is a `GeoDataFrame`
    # not a `DataFrame`in geopandas 0.9.0.
    # So there can't use `.equals` to compare the result.
    assert_frame_equal(result, expected)
