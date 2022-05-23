import pandas as pd

from dtoolkit.transformer import DataFrameTF


class FilterTF(DataFrameTF):
    """
    A transformer could get subset the dataframe rows or columns according to
    the specified index labels.

    See Also
    --------
    pandas.DataFrame.filter : This transformer's prototype method.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from dtoolkit.transformer import FilterTF
    >>> df = pd.DataFrame(np.array(([1, 2, 3], [4, 5, 6])),
    ...                   index=['mouse', 'rabbit'],
    ...                   columns=['one', 'two', 'three'])
    >>> df
            one  two  three
    mouse     1    2      3
    rabbit    4    5      6

    Select columns by name

    >>> tf = FilterTF(items=['one', 'three'])
    >>> tf.transform(df)
                one  three
    mouse     1      3
    rabbit    4      6

    Select columns by regular expression

    >>> tf = FilterTF(regex='e$', axis=1)
    >>> tf.transform(df)
                one  three
    mouse     1      3
    rabbit    4      6

    Select rows containing 'bbi'

    >>> tf = FilterTF(like='bbi', axis=0)
    >>> tf.transform(df)
                one  two  three
    rabbit    4    5      6
    """

    transform_method = staticmethod(pd.DataFrame.filter)
