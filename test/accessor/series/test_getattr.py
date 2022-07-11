import pandas as pd
import pytest

from dtoolkit.accessor.series import getattr  # noqa: F401


@pytest.mark.parametrize(
    "s, name, args, kwargs, expected",
    [
        # test attribute
        (
            pd.Series(["s1", "s2", "s3"]),
            "__doc__",
            (),
            {},
            pd.Series(["s".__doc__] * 3),
        ),
        (
            pd.Series([object, object]),
            "__name__",
            (),
            {},
            pd.Series(["object"] * 2),
        ),
        (
            pd.Series(["s1", "s2", "s3"]),
            "whatever",
            (),
            {},
            pd.Series([None] * 3),
        ),
        # test method
        (
            pd.Series(["s", "ss", "sss"]),
            "count",
            ("s",),
            {},
            pd.Series([1, 2, 3]),
        ),
        # test method
        (
            pd.Series(["s", "ss", "sss"]),
            "count",
            ("s",),
            {},
            pd.Series([1, 2, 3]),
        ),
        (
            pd.Series(["s", "ss", "sss"]),
            "count",
            ("zero",),
            {},
            pd.Series([0] * 3),
        ),
        # test kwargs
        (
            pd.Series(["s", "ss", "sss"]),
            "count",
            ("s", 0),
            {},
            pd.Series([1, 2, 3]),
        ),
        (
            pd.Series(["s", "ss", "sss"]),
            "count",
            ("s", 1),
            {},
            pd.Series([0, 1, 2]),
        ),
        (
            pd.Series(["s_{key}", "ss_{key}"]),
            "format",
            (),
            dict(key="end"),
            pd.Series(["s_end", "ss_end"]),
        ),
    ],
)
def test_attr_work(s, name, args, kwargs, expected):
    result = s.getattr(name, *args, **kwargs)

    assert result.equals(expected)
