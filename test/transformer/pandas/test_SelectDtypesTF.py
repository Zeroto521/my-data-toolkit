from test.transformer.conftest import df_iris
from test.transformer.conftest import df_label
from test.transformer.conftest import df_mixed

import pytest
from pandas.testing import assert_frame_equal

from dtoolkit.transformer import SelectDtypesTF


@pytest.mark.parametrize(
    "types, expected",
    [
        [float, df_iris],
        [int, df_label],
    ],
)
def test_work(types, expected):
    tf = SelectDtypesTF(include=types)

    result = tf.fit_transform(df_mixed)

    assert_frame_equal(result, expected)
