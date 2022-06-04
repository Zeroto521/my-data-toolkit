import pandas as pd

from dtoolkit.transformer.base import DataFrameTF


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
    >>> df = pd.DataFrame(
    ...     {
    ...         'A': range(1, 6),
    ...         'B': range(10, 0, -2),
    ...         'C C': range(10, 5, -1),
    ...     },
    ... )
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
