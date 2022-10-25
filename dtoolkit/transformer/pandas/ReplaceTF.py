import pandas as pd

from dtoolkit.transformer.base import DataFrameTF


class ReplaceTF(DataFrameTF):
    """
    A transformer could replace values given input parameters.

    See Also
    --------
    pandas.DataFrame.replace : This transformer's prototype method.

    Notes
    -----
    :meth:`~pandas.DataFrame.replace`'s ``inplace`` parameter is not work for
    this transformer. Actually this break pipeline stream. If a transformer's
    ``inplace`` is ``True``, the next tf input would get ``None``.

    Examples
    --------

    Scalar ``to_replace`` and ``value``

    >>> import pandas as pd
    >>> from dtoolkit.transformer import ReplaceTF
    >>> df = pd.DataFrame(
    ...     {
    ...         'A': [0, 1, 2, 3, 4],
    ...         'B': [5, 6, 7, 8, 9],
    ...         'C': ['a', 'b', 'c', 'd', 'e'],
    ...     },
    ... )
    >>> tf = ReplaceTF(0, 5)
    >>> tf.transform(df)
    A  B  C
    0  5  5  a
    1  1  6  b
    2  2  7  c
    3  3  8  d
    4  4  9  e

    List-like ``to_replace``

    >>> tf = ReplaceTF([0, 1, 2, 3], 4)
    >>> tf.transform(df)
    A  B  C
    0  4  5  a
    1  4  6  b
    2  4  7  c
    3  4  8  d
    4  4  9  e

    >>> tf = ReplaceTF([0, 1, 2, 3], [4, 3, 2, 1])
    >>> tf.transform(df)
    A  B  C
    0  4  5  a
    1  3  6  b
    2  2  7  c
    3  1  8  d
    4  4  9  e

    dict-like ``to_replace``

    >>> tf = ReplaceTF({0: 10, 1: 100})
    >>> tf.transform(df)
        A  B  C
    0   10  5  a
    1  100  6  b
    2    2  7  c
    3    3  8  d
    4    4  9  e

    >>> tf = ReplaceTF({'A': 0, 'B': 5}, 100)
    >>> tf.transform(df)
        A    B  C
    0  100  100  a
    1    1    6  b
    2    2    7  c
    3    3    8  d
    4    4    9  e

    >>> tf = ReplaceTF({'A': {0: 100, 4: 400}})
    >>> tf.transform(df)
        A  B  C
    0  100  5  a
    1    1  6  b
    2    2  7  c
    3    3  8  d
    4  400  9  e

    Regular expression ``to_replace``

    >>> df = pd.DataFrame(
    ...     {
    ...         'A': ['bat', 'foo', 'bait'],
    ...         'B': ['abc', 'bar', 'xyz'],
    ...     },
    ... )
    >>> tf = ReplaceTF(to_replace=r'^ba.$', value='new', regex=True)
    >>> tf.transform(df)
        A    B
    0   new  abc
    1   foo  new
    2  bait  xyz

    >>> tf = ReplaceTF({'A': r'^ba.$'}, {'A': 'new'}, regex=True)
    >>> tf.transform(df)
        A    B
    0   new  abc
    1   foo  bar
    2  bait  xyz

    >>> tf = ReplaceTF(regex=r'^ba.$', value='new')
    >>> tf.transform(df)
        A    B
    0   new  abc
    1   foo  new
    2  bait  xyz

    >>> tf = ReplaceTF(regex={r'^ba.$': 'new', 'foo': 'xyz'})
    >>> tf.transform(df)
        A    B
    0   new  abc
    1   xyz  new
    2  bait  xyz

    >>> tf = ReplaceTF(regex=[r'^ba.$', 'foo'], value='new')
    >>> tf.transform(df)
        A    B
    0   new  abc
    1   new  new
    2  bait  xyz
    """

    transform_method = staticmethod(pd.DataFrame.replace)
