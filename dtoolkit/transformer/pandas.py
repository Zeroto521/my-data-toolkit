from pandas import DataFrame

from .._checking import check_dataframe_type
from ..accessor import FilterInAccessor  # noqa
from .base import Transformer


class DataFrameTF(Transformer):
    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)


# AssignTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class AssignTF(Transformer):
    r"""
    Assign new columns to a DataFrame.

    Returns a new object with all original columns in addition to new ones.
    Existing columns that are re-assigned will be overwritten.

    Notes
    -----
    Assigning multiple columns within the same ``assign`` is possible.
    Later items in '\*\*kwargs' may refer to newly created or modified
    columns in 'df'; items are computed and assigned into 'df' in order.

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

    Where the value is a callable, evaluated on `df`:

    >>> pipeline = AssignTF(temp_f=lambda x: x.temp_c * 9 / 5 + 32)
    >>> pipeline.transform(df)
                temp_c  temp_f
    Portland    17.0    62.6
    Berkeley    25.0    77.0
    """

    def operate(self, *args, **kwargs) -> DataFrame:
        """
        Parameters
        ----------
        **kwargs : dict of {str: callable or Series}
            The column names are keywords. If the values are
            callable, they are computed on the DataFrame and
            assigned to the new columns. The callable must not
            change input DataFrame (though pandas doesn't check it).
            If the values are not callable, (e.g. a Series, scalar, or array),
            they are simply assigned.

        Returns
        -------
        DataFrame
            A new DataFrame with the new columns in addition to
            all the existing columns.
        """
        return DataFrame.assign(*args, **kwargs)


# AppendTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class AppendTF(DataFrameTF):
    """
    Append rows of `other` to the end of caller, returning a new object.

    Columns in `other` that are not in the caller are added as new columns.

    Notes
    -----
    If a list of dict/series is passed and the keys are all contained in
    the DataFrame's index, the order of the columns in the resulting
    DataFrame will be unchanged.

    Iteratively appending rows to a DataFrame can be more computationally
    intensive than a single concatenate. A better solution is to append
    those rows to a list and then concatenate the list with the original
    DataFrame all at once.

    Examples
    --------
    >>> from dtoolkit.transformer import AppendTF
    >>> import pandas as pd
    >>> df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'), index=['x', 'y'])
    >>> df
        A  B
    x  1  2
    y  3  4
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'), index=['x', 'y'])
    >>> tf = AppendTF(df2)
    >>> tf.transform(df)
        A  B
    x  1  2
    y  3  4
    x  5  6
    y  7  8

    With `ignore_index` set to `True`:

    >>> tf = AppendTF(df2, ignore_index=True)
    >>> tf.transform(df)
        A  B
    0  1  2
    1  3  4
    2  5  6
    3  7  8
    """

    def operate(self, *args, **kwargs) -> DataFrame:
        """
        Parameters
        ----------
        other : DataFrame or Series/dict-like object, or list of these
            The data to append.
        ignore_index : bool, default False
            If True, the resulting axis will be labeled 0, 1, …, n - 1.
        verify_integrity : bool, default False
            If True, raise ValueError on creating index with duplicates.
        sort : bool, default False
            Sort columns if the columns of `self` and `other` are not aligned.

        Returns
        -------
        DataFrame
            A new DataFrame consisting of the rows of caller and the rows of `other`.
        """
        return DataFrame.append(*args, **kwargs)


class DropTF(DataFrameTF):
    """
    Drop specified labels from rows or columns.

    Remove rows or columns by specifying label names and corresponding
    axis, or by specifying directly index or column names. When using a
    multi-index, labels on different levels can be removed by specifying
    the level.

    Parameters
    ----------
    labels : single label or list-like
        Index or column labels to drop.
    axis : {0 or 'index', 1 or 'columns'}, default 0
        Whether to drop labels from the index (0 or 'index') or
        columns (1 or 'columns').
    index : single label or list-like
        Alternative to specifying axis (``labels, axis=0``
        is equivalent to ``index=labels``).
    columns : single label or list-like
        Alternative to specifying axis (``labels, axis=1``
        is equivalent to ``columns=labels``).
    level : int or level name, optional
        For MultiIndex, level from which the labels will be removed.
    errors : {'ignore', 'raise'}, default 'raise'
        If 'ignore', suppress error and only existing labels are
        dropped.

    Returns
    -------
    DataFrame
        DataFrame without the removed index or column labels.

    Raises
    ------
    KeyError
        If any of the labels is not found in the selected axis.

    Notes
    -----
        `DataFrame.drop`'s `inplace` parameter is not work for transformer.

    Examples
    --------
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

    >>> tf = DropTF(['B', 'C'])
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

    def operate(self, *args, **kwargs) -> DataFrame:
        kwargs.pop("inplace", None)
        return DataFrame.drop(*args, **kwargs)


class EvalTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.eval(*args, **kwargs)


class FillnaTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.fillna(*args, **kwargs)


class FilterInTF(DataFrameTF):
    def transform(self, X, *_):
        self.validate(X)

        return X.filterin(*self.args, **self.kwargs)


class FilterTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.filter(*args, **kwargs)


class GetTF(Transformer):
    def operate(self, *args, **kwargs):
        return DataFrame.get(*args, **kwargs)


class QueryTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.query(*args, **kwargs)


class ReplaceTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.replace(*args, **kwargs)


class SelectDtypesTF(DataFrameTF):
    def operate(self, *args, **kwargs):
        return DataFrame.select_dtypes(*args, **kwargs)
