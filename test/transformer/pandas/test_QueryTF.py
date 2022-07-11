from test.transformer.conftest import df_iris
from test.transformer.conftest import feature_names

from pandas.testing import assert_frame_equal

from dtoolkit.transformer import QueryTF


def test_greater_symbol():
    tf = QueryTF(f"`{feature_names[0]}` > 0")
    result = tf.fit_transform(df_iris)

    assert_frame_equal(result, df_iris)


def test_plus_symbol():
    tf = QueryTF(f"`{'`+`'.join(feature_names)}` < 100")
    result = tf.fit_transform(df_iris)

    assert_frame_equal(result, df_iris)


def test_divide_symbol():
    tf = QueryTF(f"`{feature_names[0]}` / 100 > 1")
    result = tf.fit_transform(df_iris)

    assert len(result) == 0
