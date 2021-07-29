import joblib
import numpy as np
import pandas as pd
import pytest
from scipy import sparse
from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline

from dtoolkit.accessor import ColumnAccessor  # noqa
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

#
# Create dataset
#

iris = load_iris(as_frame=True)
feature_names = iris.feature_names
df_iris = iris.data
s = iris.target
array = df_iris.values

period_names = [f"h_{t}" for t in range(24 + 1)]
df_period = pd.DataFrame(
    np.random.randint(
        len(period_names),
        size=(len(df_iris), len(period_names)),
    ),
    columns=period_names,
)

label_size = 3
data_size = len(df_iris)
df_label = pd.DataFrame(
    {
        "a": np.random.randint(label_size, size=data_size),
        "b": np.random.randint(label_size, size=data_size),
    },
)


df_mixed = pd.concat([df_iris, df_label], axis=1)


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
            make_pipeline(GetTF("target"), RavelTF()),
        ),
    ],
)
def test_pipeline_work(name, data, pipeline):
    transformed_data = pipeline.fit_transform(data)
    pipeline.inverse_transform(transformed_data)

    joblib.dump(pipeline, f"{name}.pipeline.joblib")


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
        res = pipeline.fit_transform(df_mixed)

        assert isinstance(res, pd.DataFrame)

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

        res = pipeline.fit_transform(df_mixed)

        assert sparse.isspmatrix(res)


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

    res = tf.fit_transform(
        pd.DataFrame(
            {
                "a": [0, 1, 0],
                "b": [1, 1, 0],
            },
        ),
    )

    assert res.notnull().all(axis=None)
