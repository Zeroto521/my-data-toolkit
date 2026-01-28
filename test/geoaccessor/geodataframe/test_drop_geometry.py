import pandas as pd
import pytest

from dtoolkit.geoaccessor.geodataframe import drop_geometry  # noqa: F401


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
                pd.DataFrame(
                    {
                        "x": [122, 100],
                        "y": [55, 1],
                    },
                )
                .from_xy("x", "y")
                .drop(columns=["x", "y"])
            ),
            pd.DataFrame(index=[0, 1], columns=[]),
        ),
    ],
)
def test_work(df, expected):
    result = df.drop_geometry()

    assert expected.equals(result)
