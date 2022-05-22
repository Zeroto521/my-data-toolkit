from dtoolkit.accessor.dataframe import cols as dataframe_cols  # noqa
from dtoolkit.accessor.series import cols as series_cols  # noqa
from dtoolkit.transformer import FilterTF


def test_work():
    tf = FilterTF(regex=r"^\w+?_(1[8-9]|2[0-2])$", axis=1)

    result = tf.fit_transform(df_period)

    assert len(result.cols()) == 5
