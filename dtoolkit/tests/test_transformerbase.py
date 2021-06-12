from dtoolkit.transformer import TransformerBase


def test_fit_work():
    tf = TransformerBase()
    assert tf is tf.fit()
