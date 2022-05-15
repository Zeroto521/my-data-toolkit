import pandas as pd
import pytest

from dtoolkit.accessor.series import values_to_dict  # noqa


@pytest.mark.parametrize(
    "s, kwargs, excepted",
    [
        (
            pd.Series(range(4), index=["a", "b", "a", "c"]),
            dict(to_list=True),
            {"a": [0, 2], "b": [1], "c": [3]},
        ),
        (
            pd.Series(range(4), index=["a", "b", "a", "c"]),
            dict(to_list=False),
            {"a": [0, 2], "b": 1, "c": 3},
        ),
        (
            pd.Series(range(4), index=["a", "b", "c", "d"]),
            dict(to_list=False),
            {"a": 0, "b": 1, "c": 2, "d": 3},
        ),
        (
            pd.Series([1] * 4, index=["a", "b", "c", "d"]),
            dict(to_list=True),
            {"a": [1], "b": [1], "c": [1], "d": [1]},
        ),
        (
            pd.Series([1] * 4, index=["a", "b", "c", "d"]),
            dict(to_list=False),
            {"a": 1, "b": 1, "c": 1, "d": 1},
        ),
        (
            pd.Series(range(4), index=["a"] * 4),
            dict(to_list=True),
            {"a": [0, 1, 2, 3]},
        ),
        (
            pd.Series([1] * 4, index=["a"] * 4),
            dict(to_list=False),
            {"a": [1, 1, 1, 1]},
        ),
    ],
)
def test_work(s, kwargs, excepted):
    result = s.values_to_dict(**kwargs)

    assert result == excepted
