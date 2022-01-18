from test.transformer import df_iris
from test.transformer import df_label
from test.transformer import s

import pandas as pd
from scipy import sparse

from dtoolkit.transformer import MinMaxScaler
from dtoolkit.transformer import OneHotEncoder


class TestMinMaxscaler:
    def test_work(self):
        tf = MinMaxScaler().fit(df_iris)

        data_transformed = tf.transform(df_iris)
        data = tf.inverse_transform(data_transformed)
        data = data.round(2)

        assert df_iris.equals(data)

    def test_series_in_dataframe_out(self):
        tf = MinMaxScaler()
        tf.fit(s.to_frame())
        result = tf.inverse_transform(s)

        assert isinstance(s, pd.Series)
        assert isinstance(result, pd.DataFrame)


class TestOneHotEncoder:
    def test_dataframe_in_dataframe_out(self):
        tf = OneHotEncoder()
        result = tf.fit_transform(df_label)

        assert isinstance(result, pd.DataFrame)

    def test_return_dataframe_columns(self):
        tf = OneHotEncoder(categories_with_parent=True)
        result = tf.fit_transform(df_label)

        assert all("_" in column for column in result.columns)

    def test_sparse_is_ture(self):
        tf = OneHotEncoder(sparse=True)
        result = tf.fit_transform(df_label)

        assert sparse.isspmatrix(result)
