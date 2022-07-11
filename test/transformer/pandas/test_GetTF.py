import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

from dtoolkit.transformer import GetTF
from test.transformer.conftest import df_iris
from test.transformer.conftest import feature_names


@pytest.mark.parametrize("cols", [feature_names[0], feature_names])
def test_work(cols):
    tf = GetTF(cols)

    result = tf.fit_transform(df_iris)
    expected = df_iris[cols]

    if isinstance(expected, pd.Series):
        assert_series_equal(result, expected)
    else:
        assert_frame_equal(result, expected)
