import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.accessor.dataframe import filter_in  # noqa: F401


df = pd.DataFrame(
    {
        "legs": [2, 4, 2],
        "wings": [2, 0, 0],
    },
    index=["falcon", "dog", "cat"],
)


@pytest.mark.parametrize(
    "condition, kwargs, expected",
    [
        (
            [0, 2],
            dict(how="all", complement=False),
            pd.DataFrame(
                {
                    "legs": [2, 2],
                    "wings": [2, 0],
                },
                index=["falcon", "cat"],
            ),
        ),
        (
            [0, 2],
            dict(how="any", complement=False),
            pd.DataFrame(
                {
                    "legs": [2, 4, 2],
                    "wings": [2, 0, 0],
                },
                index=["falcon", "dog", "cat"],
            ),
        ),
        (
            [0, 2],
            dict(how="any", complement=True),
            pd.DataFrame(
                {
                    "legs": [4],
                    "wings": [0],
                },
                index=["dog"],
            ),
        ),
        (
            (0, 2),
            dict(how="all", complement=False),
            pd.DataFrame(
                {
                    "legs": [2, 2],
                    "wings": [2, 0],
                },
                index=["falcon", "cat"],
            ),
        ),
        (
            [4],
            dict(how="any", complement=False),
            pd.DataFrame(
                {
                    "legs": [4],
                    "wings": [0],
                },
                index=["dog"],
            ),
        ),
        (
            [4],
            dict(how="all", complement=True),
            pd.DataFrame(
                {
                    "legs": [2, 2],
                    "wings": [2, 0],
                },
                index=["falcon", "cat"],
            ),
        ),
        (
            {"legs": [4]},
            dict(how="all", complement=False),
            pd.DataFrame(
                {
                    "legs": [4],
                    "wings": [0],
                },
                index=["dog"],
            ),
        ),
        (
            {"legs": [4]},
            dict(how="all", complement=True),
            pd.DataFrame(
                {
                    "legs": [2, 2],
                    "wings": [2, 0],
                },
                index=["falcon", "cat"],
            ),
        ),
        (
            {"legs": [4], "wings": [0]},
            dict(how="all", complement=False),
            pd.DataFrame(
                {
                    "legs": [4],
                    "wings": [0],
                },
                index=["dog"],
            ),
        ),
        (
            {"legs": [4], "wings": [0]},
            dict(how="any", complement=False),
            pd.DataFrame(
                {
                    "legs": [4, 2],
                    "wings": [0, 0],
                },
                index=["dog", "cat"],
            ),
        ),
        (
            pd.Series([0], index=["dog"]),
            dict(how="any", complement=False),
            pd.DataFrame(
                {
                    "legs": [4],
                    "wings": [0],
                },
                index=["dog"],
            ),
        ),
        (
            pd.DataFrame({"legs": [2, 4, 2]}, index=["falcon", "dog", "cat"]),
            dict(how="all", complement=False),
            pd.DataFrame(
                {
                    "legs": [2, 4, 2],
                    "wings": [2, 0, 0],
                },
                index=["falcon", "dog", "cat"],
            ),
        ),
    ],
)
def test_work(condition, kwargs, expected):
    result = df.filter_in(condition, **kwargs)

    assert_frame_equal(result, expected)


def test_issue_145():
    # test my-data-toolkit#145
    result = df.filter_in({"legs": [2]})

    expected = pd.DataFrame(
        {
            "legs": [2, 2],
            "wings": [2, 0],
        },
        index=["falcon", "cat"],
    )

    assert_frame_equal(result, expected)
