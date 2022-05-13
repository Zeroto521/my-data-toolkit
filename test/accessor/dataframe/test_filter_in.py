from test.accessor.conftest import d

import pandas as pd

from dtoolkit.accessor.dataframe import filter_in  # noqa


def test_work():
    res = d.filter_in({"a": [0, 1], "b": [2]})

    assert res["a"].isin([0, 1]).any()  # 0 and 1 in a
    assert (~res["a"].isin([2])).all()  # 2 not in a
    assert res["b"].isin([2]).any()  # 2 in a
    assert (~res["b"].isin([0, 1])).all()  # 0 and not in a


def test_issue_145():
    # test my-data-toolkit#145
    df = pd.DataFrame(
        {
            "legs": [2, 4, 2],
            "wings": [2, 0, 0],
        },
        index=["falcon", "dog", "cat"],
    )
    res = df.filter_in({"legs": [2]})

    expected = pd.DataFrame(
        {
            "legs": [2, 2],
            "wings": [2, 0],
        },
        index=["falcon", "cat"],
    )

    assert res.equals(expected)
