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
    def operate(self, *args, **kwargs):
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
