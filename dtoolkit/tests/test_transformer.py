import joblib
import pandas as pd
import pytest

from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline

from dtoolkit.accessor import ColumnAccessor  # noqa
from dtoolkit.transformer import (
    AppendTF,
    DropTF,
    EvalTF,
    FillnaTF,
    GetTF,
    MinMaxScaler,
    QueryTF,
    RavelTF,
    _change_data_to_df,
)


iris = load_iris(as_frame=True)
feature_names = iris.feature_names
df = iris.data
s = iris.target
array = df.values


#
# Sklearn's operation test
#


@pytest.mark.parametrize("data, df", [(array, df), (array, array)])
def test_change_data_to_df(data, df):
    data_new = _change_data_to_df(data, df)

    assert type(df) is type(data_new)  # pylint: disable=unidiomatic-typecheck


def test_minmaxscaler():
    tf = MinMaxScaler().fit(df)

    data_transformed = tf.transform(df)
    data = tf.inverse_transform(data_transformed)
    data = data.round(2)

    assert df.equals(data)


#
# Pandas's operation test
#


@pytest.mark.parametrize("cols", [[feature_names[0]], feature_names])
def test_gettf(cols):
    tf = GetTF(cols)

    res = tf.fit_transform(df)
    expt = df[cols]

    assert res.equals(expt)


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


def test_appendtf():
    tf = AppendTF(other=pd.DataFrame(dict(a=range(1, 9))), ignore_index=True)

    res = tf.fit_transform(pd.DataFrame(dict(a=[0])))
    expt = pd.DataFrame(dict(a=range(9)))

    assert res.equals(expt)


#
# numpy's operation test
#


@pytest.mark.parametrize("data", [array, df, s, s.tolist()])
def test_raveltf(data):
    res = RavelTF().fit_transform(data)

    assert res.ndim == 1


#
# pipeline test
#


def gen_x_pipeline():
    return make_pipeline(
        EvalTF(f"sum = `{'` + `'.join(feature_names)}`"),
        QueryTF("sum > 10"),
        GetTF(feature_names),
        DropTF(columns=feature_names[:2]),
        MinMaxScaler(),
    )


def gen_y_pipeline():
    return make_pipeline(RavelTF())


class TestPipeline:
    def test_x_pipeline_work(self):
        pipe = gen_x_pipeline()
        transformed_data = pipe.fit_transform(df)
        data = pipe.inverse_transform(transformed_data)
        data = data.round(2)

    def test_y_pipeline_work(self):
        pipe = gen_y_pipeline()
        transformed_data = pipe.fit_transform(s)
        pipe.inverse_transform(transformed_data)


#
# pickle pipeline test
#


@pytest.mark.parametrize(
    "name,pipe", [("x", gen_x_pipeline()), ("y", gen_y_pipeline())]
)
def test_save_to_file(name, pipe):
    pipe.fit(df)

    joblib.dump(pipe, f"{name}.pipeline.joblib")
