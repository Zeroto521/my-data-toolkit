import pandas as pd
import pytest

from dtoolkit.accessor.series import values_to_dict


@pytest.mark.parametrize(
    "s, kwargs, expected",
    [
        (
            pd.Series(range(4), index=["a", "b", "a", "c"]),
            dict(unique=True, to_list=True),
            {"a": [0, 2], "b": [1], "c": [3]},
        ),
        (
            pd.Series(range(4), index=["a", "b", "a", "c"]),
            dict(unique=False, to_list=False),
            {"a": [0, 2], "b": 1, "c": 3},
        ),
        (
            pd.Series([0] * 4, index=["a", "b", "a", "c"]),
            dict(unique=True, to_list=False),
            {"a": 0, "b": 0, "c": 0},
        ),
        (
            pd.Series([0] * 4, index=["a", "b", "a", "c"]),
            dict(unique=False, to_list=False),
            {"a": [0, 0], "b": 0, "c": 0},
        ),
        (
            pd.Series([0] * 4, index=["a", "b", "a", "c"]),
            dict(unique=True, to_list=True),
            {"a": [0], "b": [0], "c": [0]},
        ),
    ],
)
def test_work(s, kwargs, expected):
    result = s.values_to_dict(**kwargs)

    assert result == expected
