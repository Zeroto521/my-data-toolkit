from functools import partial
from test.transformer import df_iris
from test.transformer import df_label
from test.transformer import df_mixed
from test.transformer import df_period
from test.transformer import feature_names
from test.transformer import s

import pandas as pd
import pytest

from dtoolkit.accessor.dataframe import cols as dataframe_cols  # noqa
from dtoolkit.accessor.series import cols as series_cols  # noqa
from dtoolkit.transformer import AppendTF
from dtoolkit.transformer import AssignTF
from dtoolkit.transformer import DropTF
from dtoolkit.transformer import EvalTF
from dtoolkit.transformer import FillnaTF
from dtoolkit.transformer import FilterInTF
from dtoolkit.transformer import FilterTF
from dtoolkit.transformer import GetTF
from dtoolkit.transformer import QueryTF
from dtoolkit.transformer import ReplaceTF
from dtoolkit.transformer import SelectDtypesTF


def test_assigntf():
    def period(df, regex):
        df_filter = df.filter(regex=regex, axis=1)
        return df_filter.sum(axis=1)

    names = ["breakfast", "lunch", "tea"]
    regexs = [r"^\w+?([6-9]|10)$", r"^\w+?1[1-4]$", r"^\w+?1[5-7]$"]
    names_regexs_dict = {
        key: partial(period, regex=regex) for key, regex in zip(names, regexs)
    }

    tf = AssignTF(**names_regexs_dict)
    res = tf.fit_transform(df_period)

    for key in names:
        assert (res[key] > 0).any()


def test_appendtf():
    tf = AppendTF(other=pd.DataFrame(dict(a=range(1, 9))), ignore_index=True)

    res = tf.fit_transform(pd.DataFrame(dict(a=[0])))
    expt = pd.DataFrame(dict(a=range(9)))

    assert res.equals(expt)


class TestDropTF:
    def setup_method(self):
        self.df_iris = df_iris.copy()

    def test_work(self):
        tf = DropTF(columns=[feature_names[0]])
        res = tf.fit_transform(self.df_iris)

        assert feature_names[0] not in res.cols()

    def test_inplace(self):
        tf = DropTF(columns=[feature_names[0]], inplace=True)

        res = tf.fit_transform(self.df_iris)

        assert res is not None
        assert feature_names[0] not in res.cols()
        assert self.df_iris.equals(df_iris)

    def test_input_is_not_series_or_dataframe(self):
        tf = DropTF(columns=feature_names)
        with pytest.raises(TypeError):
            tf.transform(1)

    def test_input_is_series(self):
        tf = DropTF(columns=s.name)
        res = tf.transform(s)

        assert len(res.columns) == 0


def test_evaltf():
    new_column = "double_value"
    tf = EvalTF(f"`{new_column}` = `{feature_names[0]}` * 2")
    res = tf.fit_transform(df_iris)

    assert res[new_column].equals(df_iris[feature_names[0]] * 2)


class TestFillnaTF:
    def setup_method(self):
        self.df = pd.DataFrame({"a": [None, 1], "b": [1, None]})

    def test_fill0(self):
        tf = FillnaTF(0)
        res = tf.fit_transform(self.df)

        assert None not in res


def test_filterintf():
    tf = FilterInTF({"a": [0]})

    res = tf.fit_transform(df_label)

    assert (~res["a"].isin([1, 2])).all()  # 1 and 2 not in a


def test_filtertf():
    tf = FilterTF(regex=r"^\w+?_(1[8-9]|2[0-2])$", axis=1)

    res = tf.fit_transform(df_period)

    assert len(res.cols()) == 5


@pytest.mark.parametrize("cols", [feature_names[0], feature_names])
def test_gettf(cols):
    tf = GetTF(cols)

    res = tf.fit_transform(df_iris)
    expt = df_iris[cols]

    assert res.equals(expt)


class TestQueryTF:
    def test_greater_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` > 0")
        res = tf.fit_transform(df_iris)

        assert res.equals(df_iris)

    def test_plus_symbol(self):
        tf = QueryTF(f"`{'`+`'.join(feature_names)}` < 100")
        res = tf.fit_transform(df_iris)

        assert res.equals(df_iris)

    def test_divide_symbol(self):
        tf = QueryTF(f"`{feature_names[0]}` / 100 > 1")
        res = tf.fit_transform(df_iris)

        assert len(res) == 0


def test_replacetf():
    tf = ReplaceTF({1: "a"})

    res = tf.fit_transform(df_label)

    assert res.isin(["a"]).any(axis=None)


@pytest.mark.parametrize(
    "types, expt",
    [
        [float, df_iris],
        [int, df_label],
    ],
)
def test_select_dtypes(types, expt):
    tf = SelectDtypesTF(include=types)

    res = tf.fit_transform(df_mixed)

    assert res.equals(expt)
