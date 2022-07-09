from test.transformer.conftest import df_label

import numpy as np
import pandas as pd
from scipy import sparse

from dtoolkit.pipeline import make_pipeline
from dtoolkit.transformer import OneHotEncoder


def test_dataframe_in_dataframe_out():
    tf = OneHotEncoder()
    result = tf.fit_transform(df_label)

    assert isinstance(result, pd.DataFrame)


def test_return_dataframe_columns():
    tf = OneHotEncoder(categories_with_parent=True)
    result = tf.fit_transform(df_label)

    assert all("_" in column for column in result.columns)


def test_sparse_is_ture():
    tf = OneHotEncoder(sparse=True)
    result = tf.fit_transform(df_label)

    assert sparse.isspmatrix(result)


def test_index():
    tf = make_pipeline(OneHotEncoder())
    data = pd.DataFrame(["a", "b", "c"], index=[0, 1, 3])
    result = tf.fit_transform(data)

    assert result.index.equals(data.index)


def test_array_in_array_out():
    tf = OneHotEncoder()
    data = [
        [1],
        [2],
    ]
    result = tf.fit_transform(data)

    assert isinstance(result, np.ndarray)
