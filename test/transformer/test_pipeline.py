from test.transformer.conftest import df_iris
from test.transformer.conftest import df_label
from test.transformer.conftest import df_mixed
from test.transformer.conftest import feature_names
from test.transformer.conftest import s

import joblib
import pandas as pd
import pytest
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa
from dtoolkit.transformer import DropTF
from dtoolkit.transformer import EvalTF
from dtoolkit.transformer import FeatureUnion
from dtoolkit.transformer import FilterInTF
from dtoolkit.transformer import GetTF
from dtoolkit.transformer import make_pipeline
from dtoolkit.transformer import make_union
from dtoolkit.transformer import OneHotEncoder
from dtoolkit.transformer import QueryTF
from dtoolkit.transformer import RavelTF


class TestPipeline:  # include `make_pipeline`
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
    def test_pipeline_work(self, name, data, pipeline):
        transformed_data = pipeline.fit(data).transform(data)
        pipeline.inverse_transform(transformed_data)

        joblib.dump(pipeline, f"{name}.pipeline.joblib")

    def test_series_input_and_series_output(self):
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
    def test_passthrough(self, pipeline, data, expected):
        result = pipeline.fit_transform(data)

        assert result.equals(expected)

    def test_inverse_transform_type(self):
        pipeline = make_pipeline(
            GetTF(["target"]),
            MinMaxScaler(),
            RavelTF(),
        )
        transformed_data = pipeline.fit_transform(pd.DataFrame(s))
        s_back = pipeline.inverse_transform(transformed_data)

        assert isinstance(s_back, pd.Series)

    def test_transformer_without_fit_transform(self):
        class no_fit_transform_method:
            def fit(self, *_):
                return self

            def transform(self, X):
                return X

        pipeline = make_pipeline(no_fit_transform_method())
        result = pipeline.fit_transform(s)

        assert result.equals(s)


class TestFeatureUnion:  # include `make_union`
    @pytest.mark.parametrize(
        "pipeline",
        [
            make_union(
                make_pipeline(
                    GetTF(df_iris.cols()),
                    MinMaxScaler(),
                ),
                make_pipeline(
                    GetTF(df_label.cols()),
                    OneHotEncoder(),
                ),
            ),
            FeatureUnion(
                [
                    (
                        "number feature",
                        make_pipeline(
                            GetTF(df_iris.cols()),
                            MinMaxScaler(),
                        ),
                    ),
                    (
                        "label feature",
                        make_pipeline(
                            GetTF(df_label.cols()),
                            OneHotEncoder(),
                        ),
                    ),
                ],
            ),
        ],
    )
    def test_work(self, pipeline):
        result = pipeline.fit_transform(df_mixed)

        assert isinstance(result, pd.DataFrame)

    def test_ndarray_hstack(self):
        pipeline = make_union(
            make_pipeline(
                GetTF(df_iris.cols()),
                MinMaxScaler(),
            ),
            make_pipeline(
                GetTF(df_label.cols()),
                OneHotEncoder(sparse=True),
            ),
        )

        result = pipeline.fit_transform(df_mixed)

        assert sparse.isspmatrix(result)


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
