import pandas as pd

from dtoolkit.transformer.base import DataFrameTF


class AssignTF(DataFrameTF):
    """
    A transformer could assign new columns to a :obj:`~pandas.DataFrame`.

    See Also
    --------
    pandas.DataFrame.assign : This transformer's prototype method.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import AssignTF
    >>> df = pd.DataFrame({'temp_c': [17.0, 25.0]},
    ...                   index=['Portland', 'Berkeley'])
    >>> df
                temp_c
    Portland    17.0
    Berkeley    25.0

    Where the value is a callable, evaluated on ``df``:

    >>> pipeline = AssignTF(temp_f=lambda x: x.temp_c * 9 / 5 + 32)
    >>> pipeline.transform(df)
                temp_c  temp_f
    Portland    17.0    62.6
    Berkeley    25.0    77.0
    """

    transform_method = staticmethod(pd.DataFrame.assign)


class AppendTF(DataFrameTF):
    """
    A transformer could append rows data to the end of caller.

    See Also
    --------
    pandas.DataFrame.append : This transformer's prototype method.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import AppendTF
    >>> df = pd.DataFrame(
    ...     [[1, 2], [3, 4]],
    ...     columns=list("AB"),
    ...     index=["x", "y"],
    ... )
    >>> df
        A  B
    x  1  2
    y  3  4
    >>> df2 = pd.DataFrame(
    ...     [[5, 6], [7, 8]],
    ...     columns=list("AB"),
    ...     index=["x", "y"],
    ... )
    >>> tf = AppendTF(df2)
    >>> tf.transform(df)
        A  B
    x  1  2
    y  3  4
    x  5  6
    y  7  8

    With ``ignore_index`` set to True:

    >>> tf = AppendTF(df2, ignore_index=True)
    >>> tf.transform(df)
        A  B
    0  1  2
    1  3  4
    2  5  6
    3  7  8
    """

    transform_method = staticmethod(pd.DataFrame.append)


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
                    big
    lama    speed   45.0
            weight  200.0
            length  1.5
    falcon  speed   320.0
            weight  1.0
            length  0.3

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


class EvalTF(DataFrameTF):
    """
    A transformer could evaluate a string describing operations on
    :obj:`~pandas.DataFrame` columns.

    See Also
    --------
    pandas.DataFrame.eval : This transformer's prototype method.

    Notes
    -----
    :meth:`~pandas.DataFrame.eval`'s ``inplace`` parameter is not work for
    this transformer. Actually this break pipeline stream. If a transformer's
    ``inplace`` is ``True``, the next tf input would get ``None``.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import EvalTF
    >>> df = pd.DataFrame({'A': range(1, 6), 'B': range(10, 0, -2)})
    >>> df
        A   B
    0  1  10
    1  2   8
    2  3   6
    3  4   4
    4  5   2
    >>> tf = EvalTF('A + B')
    >>> tf.transform(df)
    0    11
    1    10
    2     9
    3     8
    4     7
    dtype: int64

    Assignment is allowed though by default the original DataFrame is not
    modified.

    >>> tf = EvalTF('C = A + B')
    >>> tf.transform(df)
        A   B   C
    0  1  10  11
    1  2   8  10
    2  3   6   9
    3  4   4   8
    4  5   2   7
    >>> df
        A   B
    0  1  10
    1  2   8
    2  3   6
    3  4   4
    4  5   2

    Multiple columns can be assigned to using multi-line expressions:

    >>> tf = EvalTF(
    ...     '''
    ... C = A + B
    ... D = A - B
    ... '''
    ... )
    >>> tf.transform(df)
        A   B   C  D
    0  1  10  11 -9
    1  2   8  10 -6
    2  3   6   9 -3
    3  4   4   8  0
    4  5   2   7  3
    """

    transform_method = staticmethod(pd.DataFrame.eval)


class FillnaTF(DataFrameTF):
    """
    A transformer could fill ``NA``/``NaN`` values using the specified method.

    See Also
    --------
    pandas.DataFrame.fillna : This transformer's prototype method.

    Notes
    -----
    :meth:`~pandas.DataFrame.fillna`'s ``inplace`` parameter is not work for
    this transformer. Actually this break pipeline stream. If a transformer's
    ``inplace`` is ``True``, the next tf input would get ``None``.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from dtoolkit.transformer import FillnaTF
    >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
    ...                    [3, 4, np.nan, 1],
    ...                    [np.nan, np.nan, np.nan, 5],
    ...                    [np.nan, 3, np.nan, 4]],
    ...                   columns=list('ABCD'))
    >>> df
        A    B   C  D
    0  NaN  2.0 NaN  0
    1  3.0  4.0 NaN  1
    2  NaN  NaN NaN  5
    3  NaN  3.0 NaN  4

    Replace all NaN elements with 0s.

    >>> tf = FillnaTF(0)
    >>> tf.transform(df)
        A   B   C   D
    0   0.0 2.0 0.0 0
    1   3.0 4.0 0.0 1
    2   0.0 0.0 0.0 5
    3   0.0 3.0 0.0 4

    We can also propagate non-null values forward or backward.

    >>> tf = FillnaTF(method='ffill')
    >>> tf.transform(df)
        A   B   C   D
    0   NaN 2.0 NaN 0
    1   3.0 4.0 NaN 1
    2   3.0 4.0 NaN 5
    3   3.0 3.0 NaN 4

    Replace all NaN elements in column 'A', 'B', 'C', and 'D', with 0, 1,
    2, and 3 respectively.

    >>> values = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    >>> tf = FillnaTF(value=values)
    >>> tf.transform(df)
        A   B   C   D
    0   0.0 2.0 2.0 0
    1   3.0 4.0 2.0 1
    2   0.0 1.0 2.0 5
    3   0.0 3.0 2.0 4

    Only replace the first NaN element.

    >>> tf = FillnaTF(value=values, limit=1)
    >>> tf.transform(df)
        A   B   C   D
    0   0.0 2.0 2.0 0
    1   3.0 4.0 NaN 1
    2   NaN 1.0 NaN 5
    3   NaN 3.0 NaN 4
    """

    transform_method = staticmethod(pd.DataFrame.fillna)


class FilterInTF(DataFrameTF):
    """
    A transformer could filter :obj:`~pandas.DataFrame` contents.

    See Also
    --------
    dtoolkit.accessor.dataframe.filter_in : This transformer's prototype method.

    Notes
    -----
    :func:`~dtoolkit.accessor.dataframe.filter_in`'s ``inplace`` parameter is
    not work for this transformer. Actually this break pipeline stream. If a
    transformer's ``inplace`` is ``True``, the next tf input would get
    ``None``.

    Examples
    --------
    >>> from dtoolkit.transformer import FilterInTF
    >>> import pandas as pd
    >>> df = pd.DataFrame({'num_legs': [2, 4, 2], 'num_wings': [2, 0, 0]},
    ...                   index=['falcon', 'dog', 'cat'])
    >>> df
            num_legs  num_wings
    falcon         2          2
    dog            4          0
    cat            2          0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> tf = FilterInTF([0, 2])
    >>> tf.transform(df)
            num_legs  num_wings
    falcon         2          2
    cat            2          0

    Filter columns.

    >>> tf = FilterInTF([0, 2], axis=1)
    >>> tf.transform(df)
                num_wings
    falcon          2
    dog             0
    cat             0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    column separately:

    >>> tf = FilterInTF({'num_legs': [2], 'num_wings': [2]})
    >>> tf.transform(df)
            num_legs  num_wings
    falcon         2          2

    When ``values`` is a Series or DataFrame the index and column must match.
    Note that ``falcon`` does not match based on the number of legs in df2.

    >>> other = pd.DataFrame({'num_legs': [8, 2], 'num_wings': [0, 2]},
    ...                      index=['spider', 'falcon'])
    >>> other
            num_legs  num_wings
    spider         8          0
    falcon         2          2
    >>> tf = FilterInTF(other)
    >>> tf.transform(df)
            num_legs  num_wings
    falcon         2          2
    """

    from dtoolkit.accessor.dataframe import filter_in

    transform_method = staticmethod(filter_in)


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


class GetTF(DataFrameTF):
    """
    A transformer could get item from object for given key
    (ex: :obj:`~pandas.DataFrame` column).

    See Also
    --------
    pandas.DataFrame.get : This transformer's prototype method.
    """

    transform_method = staticmethod(pd.DataFrame.get)


class QueryTF(DataFrameTF):
    """
    A transformer query the columns of a :obj:`~pandas.DataFrame` with a
    boolean expression.

    See Also
    --------
    pandas.DataFrame.query : This transformer's prototype method.

    Notes
    -----
    :meth:`~pandas.DataFrame.query`'s ``inplace`` parameter is not work for
    this transformer. Actually this break pipeline stream. If a transformer's
    ``inplace`` is ``True``, the next tf input would get ``None``.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import QueryTF
    >>> df = pd.DataFrame({'A': range(1, 6),
    ...                    'B': range(10, 0, -2),
    ...                    'C C': range(10, 5, -1)})
    >>> df
        A   B  C C
    0  1  10   10
    1  2   8    9
    2  3   6    8
    3  4   4    7
    4  5   2    6
    >>> tf = QueryTF('A > B')
    >>> tf.transform(df)
        A  B  C C
    4  5  2    6

    The previous expression is equivalent to

    >>> df[df.A > df.B]
        A  B  C C
    4  5  2    6

    For columns with spaces in their name, you can use backtick quoting.

    >>> tf = QueryTF('B == `C C`')
    >>> tf.transform(df)
        A   B  C C
    0  1  10   10

    The previous expression is equivalent to

    >>> df[df.B == df['C C']]
        A   B  C C
    0  1  10   10
    """

    transform_method = staticmethod(pd.DataFrame.query)


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
    >>> df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
    ...                    'B': [5, 6, 7, 8, 9],
    ...                    'C': ['a', 'b', 'c', 'd', 'e']})
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

    >>> df = pd.DataFrame({'A': ['bat', 'foo', 'bait'],
    ...                    'B': ['abc', 'bar', 'xyz']})
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
        b
    0  True
    1  False
    2  True
    3  False
    4  True
    5  False

    >>> tf = SelectDtypesTF(include=['float64'])
    >>> tf.transform(df)
        c
    0  1.0
    1  2.0
    2  1.0
    3  2.0
    4  1.0
    5  2.0

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
