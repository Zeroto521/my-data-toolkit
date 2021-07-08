import pandas as pd
import pytest

from sklearn.datasets import load_iris

from dtoolkit._checking import istype
from dtoolkit._typing import PandasTypeList
from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.transformer import (
    DropTF,
    EvalTF,
    FillnaTF,
    MinMaxScaler,
    QueryTF,
    RavelTF,
    SelectorTF,
    change_data_to_df,
)


iris = load_iris()
feature_names = iris.feature_names
df = pd.DataFrame(iris.data, columns=feature_names)
s = df[feature_names[0]]


#
# Sklearn's operation
#


@pytest.mark.parametrize("data, df", [(iris.data, df), (iris.data, iris.data)])
def test_change_data_to_df(data, df):
    data_new = change_data_to_df(data, df)

    assert type(df) == type(data_new)


class TestMinMaxScaler:
    def setup_method(self):
        self.tf = MinMaxScaler().fit(df)

    def test_work(self):
        data_transformed = self.tf.transform(df)
        data = self.tf.inverse_transform(data_transformed)
        data = data.round(2)

        assert df.equals(data)


#
# Pandas's operation
#


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


class TestQueryTF:
    def test_greater_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` > 0")
        res = tf.fit_transform(df)

        assert res.equals(df)

    def test_plus_symbol(self):
        tf = QueryTF(f"`{'`+`'.join(feature_names)}` < 100")
        res = tf.fit_transform(df)

        assert res.equals(df)

    def test_divide_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` / 100 > 1")
        res = tf.fit_transform(df)

        assert len(res) == 0


class TestFillnaTF:
    def setup_method(self):
        self.df = pd.DataFrame({"a": [None, 1], "b": [1, None]})

    def test_fill0(self):
        tf = FillnaTF(0)
        res = tf.fit_transform(self.df)

        assert None not in res


def test_evaltf():
    new_column = "double_value"
    tf = EvalTF(f"`{new_column}` = `{feature_names[0]}` * 2")
    res = tf.fit_transform(df)

    assert res[new_column].equals(df[feature_names[0]] * 2)


def test_droptf():
    tf = DropTF(columns=[feature_names[0]])
    res = tf.fit_transform(df)

    assert feature_names[0] not in res.cols()


#
# numpy's operation
#


@pytest.mark.parametrize("data", [iris.data, df, s, s.tolist()])
def test_raveltf(data):
    res = RavelTF().fit_transform(data)

    assert res.ndim == 1
