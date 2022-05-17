import pytest

import pandas as pd

from dtoolkit.accessor.dataframe import values_to_dict  # noqa


@pytest.mark.parametrize(
    "df, kwargs, expected",
    [
        (
            pd.DataFrame(
                {
                    "x": ["A", "A", "B", "B", "B"],
                    "y": ["a", "b", "c", "d", "d"],
                    "z": ["1", "2", "3", "3", "4"],
                }
            ),
            dict(order=None, ascending=True, unique=True, to_list=True),
            {
                "A": {"a": ["1"], "b": ["2"]},
                "B": {"c": ["3"], "d": ["3", "4"]},
            },
        ),
        (
            pd.DataFrame(
                {
                    "x": ["A", "A", "B", "B", "B"],
                    "y": ["a", "b", "c", "d", "d"],
                    "z": ["1", "2", "3", "3", "4"],
                }
            ),
            dict(order=None, ascending=False, unique=True, to_list=True),
            {
                "a": {"1": ["A"]},
                "b": {"2": ["A"]},
                "c": {"3": ["B"]},
                "d": {"3": ["B"], "4": ["B"]},
            },
        ),
        (
            pd.DataFrame(
                {
                    "x": ["A", "A", "B", "B", "B"],
                    "y": ["a", "b", "c", "d", "d"],
                    "z": ["1", "2", "3", "3", "4"],
                }
            ),
            dict(order=["y", "z", "x"], ascending=True, unique=True, to_list=True),
            {
                "a": {"1": ["A"]},
                "b": {"2": ["A"]},
                "c": {"3": ["B"]},
                "d": {"3": ["B"], "4": ["B"]},
            },
        ),
        (
            pd.DataFrame(
                {
                    "x": ["A", "A", "B", "B", "B"],
                    "y": ["a", "b", "c", "d", "d"],
                    "z": ["1", "2", "3", "3", "4"],
                }
            ),
            dict(order=["x", "z"], ascending=True, unique=True, to_list=True),
            {"A": ["1", "2"], "B": ["3", "4"]},
        ),
        (
            pd.DataFrame({"x": ["A", "A", "B", "B", "B"]}),
            dict(order=None, ascending=True, unique=True, to_list=True),
            {"0": ["A"], "1": ["A"], "2": ["B"], "3": ["B"], "4": ["B"]},
        ),
    ],
)
def test_work(df, kwargs, expected):
    result = df.values_to_dict(**kwargs)

    assert result == expected
