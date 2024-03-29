from dtoolkit.transformer import ReplaceTF
from test.transformer.data import df_label


def test_work():
    tf = ReplaceTF({1: "a"})

    result = tf.fit_transform(df_label)

    assert result.isin(["a"]).any(axis=None)
