import pandas as pd

from dtoolkit.transformer import DataFrameTF


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
    >>> df = pd.DataFrame(
    ...     [
    ...         [np.nan, 2, np.nan, 0],
    ...         [3, 4, np.nan, 1],
    ...         [np.nan, np.nan, np.nan, 5],
    ...         [np.nan, 3, np.nan, 4],
    ...     ],
    ...     columns=list('ABCD'),
    ... )
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
