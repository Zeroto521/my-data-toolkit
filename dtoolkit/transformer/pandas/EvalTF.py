import pandas as pd

from dtoolkit.transformer import DataFrameTF


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
