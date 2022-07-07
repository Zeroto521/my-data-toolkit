import pandas as pd
import pytest

from dtoolkit.geoaccessor.geodataframe import drop_geometry  # noqa


@pytest.mark.parametrize(
    "df, excpected",
    [
        (
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy("x", "y"),
            pd.DataFrame({"x": [122, 100], "y": [55, 1]}),
        ),
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
        (
            (
                pd.DataFrame({"x": [122, 100], "y": [55, 1]})
                .from_xy("x", "y", drop=True)
                .to_frame()
            ),
            pd.DataFrame(index=[0, 1]),
        ),
    ],
)
def test_work(df, excpected):
    result = df.drop_geometry()

    assert result.equals(excpected)
