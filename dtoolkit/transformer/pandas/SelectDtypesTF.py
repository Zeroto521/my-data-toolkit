import pandas as pd

from dtoolkit.transformer.base import DataFrameTF


class SelectDtypesTF(DataFrameTF):
    """
    A transformer could return a subset of the :obj:`~pandas.DataFrame`'s
    columns based on the column dtypes.

    See Also
    --------
    pandas.DataFrame.select_dtypes : This transformer's prototype method.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import SelectDtypesTF
    >>> df = pd.DataFrame({'a': [1, 2] * 3,
    ...                    'b': [True, False] * 3,
    ...                    'c': [1.0, 2.0] * 3})
    >>> df
            a      b  c
    0       1   True  1.0
    1       2  False  2.0
    2       1   True  1.0
    3       2  False  2.0
    4       1   True  1.0
    5       2  False  2.0

    >>> tf = SelectDtypesTF(include='bool')
    >>> tf.transform(df)
    0     True
    1    False
    2     True
    3    False
    4     True
    5    False
    Name: b, dtype: bool

    >>> tf = SelectDtypesTF(include=['float64'])
    >>> tf.transform(df)
    0    1.0
    1    2.0
    2    1.0
    3    2.0
    4    1.0
    5    2.0
    Name: c, dtype: float64

    >>> tf = SelectDtypesTF(exclude=['int64'])
    >>> tf.transform(df)
            b    c
    0   True  1.0
    1  False  2.0
    2   True  1.0
    3  False  2.0
    4   True  1.0
    5  False  2.0
    """

    transform_method = staticmethod(pd.DataFrame.select_dtypes)
