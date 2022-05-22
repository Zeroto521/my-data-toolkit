from test.transformer.conftest import df_iris
from test.transformer.conftest import feature_names
from test.transformer.conftest import s

import pytest

from dtoolkit.transformer import DropTF


def test_work():
    tf = DropTF(columns=[feature_names[0]])
    result = tf.fit_transform(df_iris)

    assert feature_names[0] not in result.cols()


def test_inplace():
    tf = DropTF(columns=[feature_names[0]], inplace=True)

    result = tf.fit_transform(df_iris)

    assert result is not None
    assert feature_names[0] not in result.cols()
    assert df_iris.equals(df_iris)


def test_input_is_not_series_or_dataframe():
    tf = DropTF(columns=feature_names)
    with pytest.raises(TypeError):
        tf.transform(1)


def test_input_is_series():
    tf = DropTF(columns=s.name)
    result = tf.transform(s)

    assert len(result.columns) == 0
