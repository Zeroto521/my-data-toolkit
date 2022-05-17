import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method


@register_dataframe_method
def unique(df: pd.DataFrame) -> dict:
    """
    Return a :keyword:`dict` contains each column's unique elements.

    Returns
    -------
    dict
        ``{column name, column's unique elements}``

    See Also
    --------
    pandas.dataframe.nunique

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    ...     {
    ...         "x" : ["A", "A", "B", "B", "B"],
    ...         "y" : ["a", "b", "c", "d", "d"],
    ...         "z" : ["1", "2", "3", "3", "4"],
    ...     }
    ... )
    >>> df
       x  y  z
    0  A  a  1
    1  A  b  2
    2  B  c  3
    3  B  d  3
    4  B  d  4
    >>> df.unique()
    {'x': ['A', 'B'], 'y': ['a', 'b', 'c', 'd'], 'z': ['1', '2', '3', '4']}
    """

    return {label: content.unique().tolist() for label, content in df.iteritems()}
