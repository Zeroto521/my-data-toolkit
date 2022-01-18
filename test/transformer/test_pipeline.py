from test.transformer import df_iris
from test.transformer import df_label
from test.transformer import df_mixed
from test.transformer import feature_names
from test.transformer import s

import joblib
import pandas as pd
import pytest
from scipy import sparse
from sklearn.pipeline import make_pipeline

from dtoolkit.accessor.dataframe import cols  # noqa
from dtoolkit.accessor.series import cols  # noqa
from dtoolkit.transformer import DropTF
from dtoolkit.transformer import EvalTF
from dtoolkit.transformer import FeatureUnion
from dtoolkit.transformer import FilterInTF
from dtoolkit.transformer import GetTF
from dtoolkit.transformer import make_union
from dtoolkit.transformer import MinMaxScaler
from dtoolkit.transformer import OneHotEncoder
from dtoolkit.transformer import QueryTF
from dtoolkit.transformer import RavelTF


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
    transformed_data = pipeline.fit_transform(data)
    pipeline.inverse_transform(transformed_data)

    joblib.dump(pipeline, f"{name}.pipeline.joblib")


def test_inverse_transform_type():
    pipeline = make_pipeline(
        GetTF(["target"]),
        MinMaxScaler(),
        RavelTF(),
    )
    transformed_data = pipeline.fit_transform(pd.DataFrame(s))
    s_back = pipeline.inverse_transform(transformed_data)

    assert isinstance(s_back, pd.Series)


class TestFeatureUnion:
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

    assert result.notnull().all(axis=None)
