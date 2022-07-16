import pandas as pd

from dtoolkit.transformer import DataFrameTF


class DropTF(DataFrameTF):
    """
    A transformer could drop specified labels from rows or columns.

    See Also
    --------
    pandas.DataFrame.drop : This transformer's prototype method.

    Notes
    -----
    :meth:`~pandas.DataFrame.drop`'s ``inplace`` parameter is not work for
    this transformer. Actually this break pipeline stream. If a transformer's
    ``inplace`` is ``True``, the next tf input would get ``None``.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from dtoolkit.transformer import DropTF
    >>> df = pd.DataFrame(np.arange(12).reshape(3, 4),
    ...                   columns=['A', 'B', 'C', 'D'])
    >>> df
        A  B   C   D
    0  0  1   2   3
    1  4  5   6   7
    2  8  9  10  11

    Drop columns

    >>> tf = DropTF(['B', 'C'], axis=1)
    >>> tf.transform(df)
        A   D
    0  0   3
    1  4   7
    2  8  11

    Drop a row by index

    >>> tf = DropTF([0, 1])
    >>> tf.transform(df)
        A  B   C   D
    2  8  9  10  11

    Drop columns and/or rows of MultiIndex DataFrame

    >>> midx = pd.MultiIndex(levels=[['lama', 'cow', 'falcon'],
    ...                              ['speed', 'weight', 'length']],
    ...                      codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
    ...                             [0, 1, 2, 0, 1, 2, 0, 1, 2]])
    >>> df = pd.DataFrame(index=midx, columns=['big', 'small'],
    ...                   data=[[45, 30], [200, 100], [1.5, 1], [30, 20],
    ...                         [250, 150], [1.5, 0.8], [320, 250],
    ...                         [1, 0.8], [0.3, 0.2]])
    >>> df
                    big     small
    lama    speed   45.0    30.0
            weight  200.0   100.0
            length  1.5     1.0
    cow     speed   30.0    20.0
            weight  250.0   150.0
            length  1.5     0.8
    falcon  speed   320.0   250.0
            weight  1.0     0.8
            length  0.3     0.2

    >>> tf = DropTF(index='cow', columns='small')
    >>> tf.transform(df)
    lama    speed      45.0
            weight    200.0
            length      1.5
    falcon  speed     320.0
            weight      1.0
            length      0.3
    Name: big, dtype: float64

    >>> tf = DropTF(index='length', level=1)
    >>> tf.transform(df)
                    big     small
    lama    speed   45.0    30.0
            weight  200.0   100.0
    cow     speed   30.0    20.0
            weight  250.0   150.0
    falcon  speed   320.0   250.0
            weight  1.0     0.8
    """

    transform_method = staticmethod(pd.DataFrame.drop)
