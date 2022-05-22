import pytest

from test.transformer.conftest import df_iris
from test.transformer.conftest import feature_names

from dtoolkit.transformer import GetTF


@pytest.mark.parametrize("cols", [feature_names[0], feature_names])
def test_work(cols):
    tf = GetTF(cols)

    result = tf.fit_transform(df_iris)
    expected = df_iris[cols]

    assert result.equals(expected)
