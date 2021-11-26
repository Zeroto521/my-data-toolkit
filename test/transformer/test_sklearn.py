import pandas as pd
from scipy import sparse

from test.transformer import df_iris
from test.transformer import df_label
from test.transformer import s
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
        res = tf.inverse_transform(s)

        assert isinstance(s, pd.Series)
        assert isinstance(res, pd.DataFrame)


class TestOneHotEncoder:
    def test_dataframe_in_dataframe_out(self):
        tf = OneHotEncoder()
        res = tf.fit_transform(df_label)

        assert isinstance(res, pd.DataFrame)

    def test_return_dataframe_columns(self):
        tf = OneHotEncoder(categories_with_parent=True)
        res = tf.fit_transform(df_label)

        assert all("_" in column for column in res.columns)

    def test_sparse_is_ture(self):
        tf = OneHotEncoder(sparse=True)
        res = tf.fit_transform(df_label)

        assert sparse.isspmatrix(res)
