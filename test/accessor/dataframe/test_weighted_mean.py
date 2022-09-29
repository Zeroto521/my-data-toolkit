import pandas as pd
import pytest

from dtoolkit.accessor.dataframe import weighted_mean


@pytest.mark.parametrize(
    "df, weights, validate, top, error",
    [
        # weights (Series) its index > df.columns
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            pd.Series({"a": 1, "b": 2, "c": 3}),
            False,
            1,
            KeyError,
        ),
        # weights (dict) its .keys() > df.columns
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": 1, "b": 2, "c": 3},
            False,
            1,
            KeyError,
        ),
        # weights (int)
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            1,
            False,
            1,
            TypeError,
        ),
        # weights (string)
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            "string",
            False,
            1,
            TypeError,
        ),
        # weights (dict) its values of sub-element are string
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"ab": {"a": "string"}},
            False,
            1,
            TypeError,
        ),
        # weights (dict) its values are string
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": "string"},
            False,
            1,
            TypeError,
        ),
        # sum(weights) != top
        (
            pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            {"a": 1, "b": 2},
            True,
            4,
            ValueError,
        ),
    ],
)
def test_error(df, weights, validate, top, error):
    with pytest.raises(error):
        weighted_mean(df, weights, validate=validate, top=top)
