from functools import partial

from dtoolkit.transformer import AssignTF
from test.transformer.data import df_period


def period(df, regex):
    df_filter = df.filter(regex=regex, axis=1)
    return df_filter.sum(axis=1)


def test_work():
    names = ["breakfast", "lunch", "tea"]
    regexs = [r"^\w+?([6-9]|10)$", r"^\w+?1[1-4]$", r"^\w+?1[5-7]$"]
    names_regexs_dict = {
        key: partial(period, regex=regex) for key, regex in zip(names, regexs)
    }

    tf = AssignTF(**names_regexs_dict)
    result = tf.fit_transform(df_period)

    for key in names:
        assert (result[key] > 0).any()
