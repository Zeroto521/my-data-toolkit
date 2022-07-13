from dtoolkit.accessor.dataframe import filter_in
from dtoolkit.transformer import DataFrameTF


class FilterInTF(DataFrameTF):
    """
    A transformer could filter :obj:`~pandas.DataFrame` contents.

    See Also
    --------
    dtoolkit.accessor.dataframe.filter_in : This transformer's prototype method.

    Examples
    --------
    >>> from dtoolkit.transformer import FilterInTF
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         'legs': [2, 4, 2],
    ...         'wings': [2, 0, 0],
    ...     },
    ...     index=['falcon', 'dog', 'cat'],
    ... )
    >>> df
            legs  wings
    falcon     2      2
    dog        4      0
    cat        2      0

    When ``condition`` is a list check whether every value in the DataFrame is
    present in the list (which animals have 0 or 2 legs or wings).

    Filter rows.

    >>> tf = FilterInTF([0, 2])
    >>> tf.transform(df)
            legs  wings
    falcon     2      2
    cat        2      0

    When ``condition`` is a :obj:`dict`, we can pass values to check for each
    column separately:

    >>> tf = FilterInTF({'legs': [2], 'wings': [2]})
    >>> tf.transform(df)
            legs  wings
    falcon     2      2

    When ``values`` is a Series or DataFrame the index and column must match.
    Note that ``falcon`` does not match based on the number of legs in df2.

    >>> other = pd.DataFrame({'legs': [8, 2], 'wings': [0, 2]},
    ...                      index=['spider', 'falcon'])
    >>> other
            legs  wings
    spider     8      0
    falcon     2      2
    >>> tf = FilterInTF(other)
    >>> tf.transform(df)
            legs  wings
    falcon     2      2
    """

    transform_method = staticmethod(filter_in)
