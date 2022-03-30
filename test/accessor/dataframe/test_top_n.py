import numpy as np
import pandas as pd
import pytest

import dtoolkit.accessor.dataframe  # noqa


@pytest.mark.parametrize(
    "n, largest, keep, prefix, delimiter, element, excepted",
    [
        (
            1,
            True,
            "first",
            "top",
            "_",
            "both",
            {
                "top_1": [
                    ("b", 3),
                    ("a", 3),
                    ("c", 3),
                ],
            },
        ),
        (  # test 'n'
            2,
            True,
            "first",
            "top",
            "_",
            "both",
            {
                "top_1": [("b", 3), ("a", 3), ("c", 3)],
                "top_2": [("c", 2), ("b", 2), ("a", 2)],
            },
        ),
        (  # test 'largest'
            1,
            False,
            "first",
            "top",
            "_",
            "both",
            {
                "top_1": [("a", 1), ("c", 1), ("b", 1)],
            },
        ),
        (  # test 'prefix' and 'delimiter'
            1,
            True,
            "first",
            "largest",
            "-",
            "both",
            {
                "largest-1": [
                    ("b", 3),
                    ("a", 3),
                    ("c", 3),
                ],
            },
        ),
        (  # test 'element'
            2,
            True,
            "first",
            "top",
            "_",
            "index",
            {
                "top_1": ["b", "a", "c"],
                "top_2": ["c", "b", "a"],
            },
        ),
        (  # test 'element'
            2,
            True,
            "first",
            "top",
            "_",
            "value",
            {
                "top_1": [3, 3, 3],
                "top_2": [2, 2, 2],
            },
        ),
    ],
)
def test_single_index_work(
    n,
    largest,
    keep,
    prefix,
    delimiter,
    element,
    excepted,
):
    df = pd.DataFrame(
        {
            "a": [1, 3, 2],
            "b": [3, 2, 1],
            "c": [2, 1, 3],
        },
    )

    result = df.top_n(
        n=n,
        largest=largest,
        keep=keep,
        prefix=prefix,
        delimiter=delimiter,
        element=element,
    )

    excepted = pd.DataFrame(excepted)
    assert result.equals(excepted)

@pytest.mark.parametrize(
    "n, keep, excepted",
    [
        (
            1,
            "first",
            {
                "top_1": [("c", 3), ("a", 3)],
            },
        ),
        (
            1,
            "all",
            {
                "top_1": [("c", 3), ("a", 3)],
                "top_2": [np.nan, ("b", 3)],
                "top_3": [np.nan, ("c", 3)],
            },
        ),
    ],
)
def test_duplicate_dataframe(n, keep, excepted):
    df = pd.DataFrame(
        {
            "a": [1, 3],
            "b": [2, 3],
            "c": [3, 3],
        },
    )

    result = df.top_n(n=n, keep=keep, element="both")
    excepted = pd.DataFrame(excepted)

    assert result.equals(excepted)

@pytest.mark.parametrize(
    "df, n, excepted",
    [
        (
            {
                ("a1", "a2"): [1, 3],
                ("b1", "b2"): [2, 3],
                ("c1", "c2"): [3, 3],
            },
            1,
            {
                "top_1": [
                    (("c1", "c2"), 3),
                    (("a1", "a2"), 3),
                ],
            },
        ),
        (
            {
                ("a1", "a2"): [1, 3],
                ("b1", "b2"): [2, 2],
                ("c1", "c2"): [3, 1],
            },
            2,
            {
                "top_1": [
                    (("c1", "c2"), 3),
                    (("a1", "a2"), 3),
                ],
                "top_2": [
                    (("b1", "b2"), 2),
                    (("b1", "b2"), 2),
                ],
            },
        ),
    ],
)
def test_multi_index(df, n, excepted):
    df = pd.DataFrame(df)
    result = df.top_n(n=n, element="both")
    excepted = pd.DataFrame(excepted)

    assert result.equals(excepted)

def test_element_error():
    df = pd.DataFrame(
        {
            "a": [1, 3, 2],
            "b": [3, 2, 1],
            "c": [2, 1, 3],
        },
    )

    with pytest.raises(ValueError):
        df.top_n(1, element="whatever")

