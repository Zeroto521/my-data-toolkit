from test.transformer.conftest import df_iris
from test.transformer.conftest import df_label
from test.transformer.conftest import df_mixed

import pandas as pd
import pytest
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler

from dtoolkit.accessor.dataframe import cols  # noqa: F401
from dtoolkit.accessor.series import cols  # noqa: F401
from dtoolkit.pipeline import FeatureUnion
from dtoolkit.pipeline import make_pipeline
from dtoolkit.pipeline import make_union
from dtoolkit.transformer import GetTF
from dtoolkit.transformer import OneHotEncoder


# include `make_union`
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
def test_work(pipeline):
    result = pipeline.fit_transform(df_mixed)

    assert isinstance(result, pd.DataFrame)


def test_ndarray_hstack():
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
