from dtoolkit.transformer import FilterInTF
from test.transformer.data import df_label


def test_work():
    tf = FilterInTF({"a": [0]})

    result = tf.fit_transform(df_label)

    assert (~result["a"].isin([1, 2])).all()  # 1 and 2 not in a
