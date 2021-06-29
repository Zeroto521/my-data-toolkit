import pandas as pd
import pytest
from dtoolkit._typing import PandasTypeList
from dtoolkit.transformer import SelectorTF, TransformerBase
from sklearn.datasets import load_iris

# -----------------------------------------------------------------------------
# TransformerBase test
# -----------------------------------------------------------------------------


def test_transformbase():
    tf = TransformerBase()
    assert tf is tf.fit()


# -----------------------------------------------------------------------------
# SelectorTF test
# -----------------------------------------------------------------------------


iris = load_iris()
feature_names = iris.feature_names
df = pd.DataFrame(iris.data, columns=feature_names)


@pytest.mark.parametrize("cols", [feature_names[0], feature_names[1:]])
def test_transform(cols):
    tf = SelectorTF(cols)
    assert all(tf.transform(df) == df[cols])


@pytest.mark.parametrize("cols", [feature_names[0], feature_names[1:]])
def test_fit_transform(cols):
    tf = SelectorTF(cols)
    assert all(tf.fit_transform(df) == df[cols])


@pytest.mark.parametrize("X", [iris, df])
@pytest.mark.parametrize("cols", [None, feature_names])
def test_inverse_transform(X, cols):
    tf = SelectorTF(cols)
    if isinstance(X, tuple(PandasTypeList)):
        assert all(X == tf.inverse_transform(X))
    else:
        assert X == tf.inverse_transform(X)


def test_data_is_not_dataframe():
    with pytest.raises(TypeError):
        SelectorTF().transform(iris.data)
