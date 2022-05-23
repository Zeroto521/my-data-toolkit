import pandas as pd

from dtoolkit.transformer import DataFrameTF


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
