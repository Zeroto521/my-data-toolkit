from test.transformer.conftest import df_iris
from test.transformer.conftest import feature_names
from pandas.testing import assert_series_equal

from dtoolkit.transformer import EvalTF


def test_work():
    new_column = "double_value"
    tf = EvalTF(f"`{new_column}` = `{feature_names[0]}` * 2")
    result = tf.fit_transform(df_iris)

    assert_series_equal(
        result[new_column],
        df_iris[feature_names[0]] * 2,
        check_names=False,
    )
