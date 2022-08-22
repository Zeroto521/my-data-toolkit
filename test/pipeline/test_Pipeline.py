import pytest

pytest.importorskip("sklearn")

import joblib
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal
from sklearn.preprocessing import MinMaxScaler

from dtoolkit.accessor.dataframe import cols  # noqa: F401
from dtoolkit.accessor.series import cols  # noqa: F401, F811
from dtoolkit.pipeline import make_pipeline
from dtoolkit.pipeline import make_union
from dtoolkit.transformer import DropTF
from dtoolkit.transformer import EvalTF
from dtoolkit.transformer import FilterInTF
from dtoolkit.transformer import GetTF
from dtoolkit.transformer import QueryTF
from dtoolkit.transformer import RavelTF
from test.transformer.conftest import df_iris
from test.transformer.conftest import df_mixed
from test.transformer.conftest import feature_names
from test.transformer.conftest import s


# include `make_pipeline`
@pytest.mark.parametrize(
    "name, data, pipeline",
    [
        (
            "xiris",
            df_iris,
            make_pipeline(
                EvalTF(f"`sum_feature` = `{'` + `'.join(feature_names)}`"),
                QueryTF("`sum_feature` > 10"),
                GetTF(feature_names),
                DropTF(columns=feature_names[:2]),
                MinMaxScaler(),
            ),
        ),
        (
            "yiris",
            pd.DataFrame(s),
            make_pipeline(
                GetTF(["target"]),
                MinMaxScaler(),
                RavelTF(),
            ),
        ),
        (
            "mixed",
            df_mixed,
            make_union(
                make_pipeline(
                    GetTF(["a"]),
                    FilterInTF({"a": [0]}),
                ),
                make_pipeline(
                    GetTF(["b"]),
                    FilterInTF({"b": [1]}),
                ),
            ),
        ),
    ],
)
def test_pipeline_work(name, data, pipeline):
    transformed_data = pipeline.fit(data).transform(data)
    pipeline.inverse_transform(transformed_data)

    joblib.dump(pipeline, f"{name}.pipeline.joblib")


def test_series_input_and_series_output():
    pipeline = make_pipeline(
        MinMaxScaler(),
    )
    result = pipeline.fit_transform(s)

    assert isinstance(result, pd.Series)


@pytest.mark.parametrize(
    "pipeline, data, expected",
    [
        (
            make_pipeline("passthrough"),
            df_iris,
            df_iris,
        ),
        (
            make_pipeline(None),
            df_iris,
            df_iris,
        ),
        (
            make_pipeline(None, "passthrough"),
            df_iris,
            df_iris,
        ),
        (
            make_pipeline(
                GetTF(feature_names[:2]),
                None,
            ),
            df_iris,
            df_iris.get(feature_names[:2]),
        ),
    ],
)
def test_passthrough(pipeline, data, expected):
    result = pipeline.fit_transform(data)

    assert_frame_equal(result, expected)


def test_inverse_transform_type():
    pipeline = make_pipeline(
        GetTF(["target"]),
        MinMaxScaler(),
        RavelTF(),
    )
    transformed_data = pipeline.fit_transform(pd.DataFrame(s))
    s_back = pipeline.inverse_transform(transformed_data)

    assert isinstance(s_back, pd.Series)


def test_transformer_without_fit_transform():
    class no_fit_transform_method:
        def fit(self, *_):
            return self

        def transform(self, X):
            return X

    pipeline = make_pipeline(no_fit_transform_method())
    result = pipeline.fit_transform(s)

    assert_series_equal(result, s)


def test_issue_87():
    tf = make_union(
        make_pipeline(
            GetTF(["a"]),
            FilterInTF({"a": [0]}),
        ),
        make_pipeline(
            GetTF(["b"]),
            FilterInTF({"b": [1]}),
        ),
    )

    result = tf.fit_transform(
        pd.DataFrame(
            {
                "a": [0, 1, 0],
                "b": [1, 1, 0],
            },
        ),
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.notnull().all(axis=None)
