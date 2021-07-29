import pandas as pd
import pytest
from scipy import sparse

from . import array
from . import df_iris
from . import df_label
from dtoolkit.transformer import _change_data_to_df
from dtoolkit.transformer import MinMaxScaler
from dtoolkit.transformer import OneHotEncoder

#
# Create dataset
#


@pytest.mark.parametrize("data, df", [(array, df_iris), (array, array)])
def test_change_data_to_df(data, df):
    data_new = _change_data_to_df(data, df)

    assert type(df) is type(data_new)  # pylint: disable=unidiomatic-typecheck


def test_minmaxscaler():
    tf = MinMaxScaler().fit(df_iris)

    data_transformed = tf.transform(df_iris)
    data = tf.inverse_transform(data_transformed)
    data = data.round(2)

    assert df_iris.equals(data)


class TestOneHotEncoder:
    def test_dataframe_in_dataframe_out(self):
        tf = OneHotEncoder()
        res = tf.fit_transform(df_label)

        assert isinstance(res, pd.DataFrame)

    def test_sparse_is_ture(self):
        tf = OneHotEncoder(sparse=True)
        res = tf.fit_transform(df_label)

        assert sparse.isspmatrix(res)
