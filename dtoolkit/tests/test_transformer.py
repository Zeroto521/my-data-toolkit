import pandas as pd
import pytest
from dtoolkit._checking import istype
from dtoolkit._typing import PandasTypeList
from dtoolkit.transformer import (
    EvalTF,
    QueryTF,
    RavelTF,
    SelectorTF,
    TransformerBase
)
from sklearn.datasets import load_iris


def test_transformbase():
    tf = TransformerBase()
    assert tf is tf.fit()


iris = load_iris()
feature_names = iris.feature_names
df = pd.DataFrame(iris.data, columns=feature_names)
s = df[feature_names[0]]


class TestSelectorTF:
    @pytest.mark.parametrize("cols", [feature_names, feature_names[0]])
    def test_init(self, cols):
        tf = SelectorTF(cols)
        assert isinstance(tf.cols, list)

    @pytest.mark.parametrize("cols", [[feature_names[0]], feature_names[1:]])
    def test_fit_transform(self, cols):
        tf = SelectorTF(cols)
        assert df[cols].equals(tf.fit_transform(df))

    @pytest.mark.parametrize("X", [iris, df])
    @pytest.mark.parametrize("cols", [None, feature_names])
    def test_inverse_transform(self, X, cols):
        tf = SelectorTF(cols)
        if istype(X, PandasTypeList):
            assert X.equals(tf.inverse_transform(X))
        else:
            assert X == tf.inverse_transform(X)

    def test_data_is_not_dataframe(self):
        with pytest.raises(TypeError):
            SelectorTF().transform(iris.data)


@pytest.mark.parametrize("data", [iris.data, df, s, s.tolist()])
def test_raveltf(data):
    transformed_data = RavelTF.transform(data)
    assert transformed_data.ndim == 1


class TestQueryTF:
    def test_greater_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` > 0")
        res = tf.transform(df)

        assert res.equals(df)

    def test_plus_symbol(self):
        tf = QueryTF(f"`{'`+`'.join(feature_names)}` < 100")
        res = tf.transform(df)

        assert res.equals(df)

    def test_divide_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` / 100 > 1")
        res = tf.transform(df)

        assert len(res) == 0


class TestEvalTF:
    def test_double_value(self):
        new_column = "double_value"
        tf = EvalTF(f"`{new_column}` = `{feature_names[0]}` * 2")
        res = tf.transform(df)

        assert res[new_column].equals(df[feature_names[0]] * 2)
