import pytest

from dtoolkit.transformer._util import transform_array_to_frame
from test.transformer.conftest import array
from test.transformer.conftest import df_iris


@pytest.mark.parametrize(
    "data, df",
    [
        (array, df_iris),
        (array, array),
    ],
)
def test_transform_array_to_frame(data, df):
    data_new = transform_array_to_frame(data, df)

    assert type(df) is type(data_new)  # pylint: disable=unidiomatic-typecheck
