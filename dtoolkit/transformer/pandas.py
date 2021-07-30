from pandas import DataFrame

from .._checking import check_dataframe_type
from .._typing import Pd
from ..accessor import FilterInAccessor  # noqa
from .base import Transformer


class DataFrameTF(Transformer):
    pd_method: str

    def __init__(self, *args, **kwargs):
        kwargs.pop("inplace", None)
        super().__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        return check_dataframe_type(*args, **kwargs)

    def operate(self, X: DataFrame, *args, **kwargs) -> Pd:
        return getattr(X, self.pd_method)(*args, **kwargs)


# AssignTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class AssignTF(DataFrameTF):
    r"""
    Assign new columns to a DataFrame.

    Returns a new object with all original columns in addition to new ones.
    Existing columns that are re-assigned will be overwritten.

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

    pd_method = "assign"


# AppendTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class AppendTF(DataFrameTF):
    """
    Append rows of `other` to the end of caller, returning a new object.

    Columns in `other` that are not in the caller are added as new columns.

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
        A new DataFrame consisting of the rows of caller and the rows of
        `other`.

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

    With `ignore_index` set to `True`:

    >>> tf = AppendTF(df2, ignore_index=True)
    >>> tf.transform(df)
        A  B
    0  1  2
    1  3  4
    2  5  6
    3  7  8
    """

    pd_method = "append"


# DropTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


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
    Actually this break pipeline stream. If a transformer's `inplace` is
    `True`, the next tf input would get `None`.

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

    pd_method = "drop"


# EvalTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class EvalTF(DataFrameTF):
    """
    Evaluate a string describing operations on DataFrame columns.

    Operates on columns only, not specific rows or elements.  This allows
    `eval` to run arbitrary code, which can make you vulnerable to code
    injection if you pass user input to this function.

    Parameters
    ----------
    expr : str
        The expression string to evaluate.
    **kwargs
        See the documentation for :func:`eval` for complete details
        on the keyword arguments accepted by :meth:`~pandas.DataFrame.query`.

    Returns
    -------
    ndarray, scalar, pandas object
        The result of the evaluation

    Notes
    -----
    `DataFrame.eval`'s `inplace` parameter is not work for transformer.
    Actually this break pipeline stream. If a transformer's `inplace` is
    `True`, the next tf input would get `None`.

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

    pd_method = "eval"


# FillnaTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class FillnaTF(DataFrameTF):
    """
    Fill NA/NaN values using the specified method.

    Parameters
    ----------
    value : scalar, dict, Series, or DataFrame
        Value to use to fill holes (e.g. 0), alternately a
        dict/Series/DataFrame of values specifying which value to use for
        each index (for a Series) or column (for a DataFrame).  Values not
        in the dict/Series/DataFrame will not be filled. This value cannot
        be a list.
    method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
        Method to use for filling holes in reindexed Series
        pad / ffill: propagate last valid observation forward to next valid
        backfill / bfill: use next valid observation to fill gap.
    axis : {0 or 'index', 1 or 'columns'}
        Axis along which to fill missing values.
    limit : int, default None
        If method is specified, this is the maximum number of consecutive
        NaN values to forward/backward fill. In other words, if there is
        a gap with more than this number of consecutive NaNs, it will only
        be partially filled. If method is not specified, this is the
        maximum number of entries along the entire axis where NaNs will be
        filled. Must be greater than 0 if not None.
    downcast : dict, default is None
        A dict of item->dtype of what to downcast if possible,
        or the string 'infer' which will try to downcast to an appropriate
        equal type (e.g. float64 to int64 if possible).

    Returns
    -------
    DataFrame or None
        Object with missing values filled.

    Notes
    -----
    `DataFrame.fillna`'s `inplace` parameter is not work for transformer.
    Actually this break pipeline stream. If a transformer's `inplace` is
    `True`, the next tf input would get `None`.

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

    pd_method = "fillna"


class FilterInTF(DataFrameTF):
    pd_method = "filterin"


# FilterTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/generic.py


class FilterTF(DataFrameTF):
    """
    Subset the dataframe rows or columns according to the specified index
    labels.

    Note that this routine does not filter a dataframe on its
    contents. The filter is applied to the labels of the index.

    Parameters
    ----------
    items : list-like
        Keep labels from axis which are in items.
    like : str
        Keep labels from axis for which "like in label == True".
    regex : str (regular expression)
        Keep labels from axis for which re.search(regex, label) == True.
    axis : {0 or ‘index’, 1 or ‘columns’, None}, default None
        The axis to filter on, expressed either as an index (int)
        or axis name (str). By default this is the info axis,
        'index' for Series, 'columns' for DataFrame.

    Returns
    -------
    same type as input object

    Notes
    -----
    The ``items``, ``like``, and ``regex`` parameters are
    enforced to be mutually exclusive.

    ``axis`` defaults to the info axis that is used when indexing
    with ``[]``.

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

    pd_method = "filter"


# GetTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/generic.py


class GetTF(DataFrameTF):
    """
    Get item from object for given key (ex: DataFrame column).

    Returns default value if not found.

    Parameters
    ----------
    key : object

    Returns
    -------
    value : same type as items contained in object
    """

    pd_method = "get"


# QueryTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class QueryTF(DataFrameTF):
    """
    Query the columns of a DataFrame with a boolean expression.

    Parameters
    ----------
    expr : str
        The query string to evaluate.

        You can refer to variables
        in the environment by prefixing them with an '@' character like
        ``@a + b``.

        You can refer to column names that are not valid Python variable names
        by surrounding them in backticks. Thus, column names containing spaces
        or punctuations (besides underscores) or starting with digits must be
        surrounded by backticks. (For example, a column named "Area (cm^2)"
        would be referenced as ```Area (cm^2)```). Column names which are
        Python keywords (like "list", "for", "import", etc) cannot be used.

        For example, if one of your columns is called ``a a`` and you want
        to sum it with ``b``, your query should be ```a a` + b``.

    **kwargs
        See the documentation for :func:`eval` for complete details
        on the keyword arguments accepted by :meth:`DataFrame.query`.

    Returns
    -------
    DataFrame
        DataFrame resulting from the provided query expression.

    Notes
    -----
    `DataFrame.query`'s `inplace` parameter is not work for transformer.
    Actually this break pipeline stream. If a transformer's `inplace` is
    `True`, the next tf input would get `None`.

    The result of the evaluation of this expression is first passed to
    :attr:`DataFrame.loc` and if that fails because of a
    multidimensional key (e.g., a DataFrame) then the result will be passed
    to :meth:`DataFrame.__getitem__`.

    This method uses the top-level :func:`eval` function to
    evaluate the passed query.

    The :meth:`~pandas.DataFrame.query` method uses a slightly
    modified Python syntax by default. For example, the ``&`` and ``|``
    (bitwise) operators have the precedence of their boolean cousins,
    :keyword:`and` and :keyword:`or`. This *is* syntactically valid Python,
    however the semantics are different.

    You can change the semantics of the expression by passing the keyword
    argument ``parser='python'``. This enforces the same semantics as
    evaluation in Python space. Likewise, you can pass ``engine='python'``
    to evaluate an expression using Python itself as a backend. This is not
    recommended as it is inefficient compared to using ``numexpr`` as the
    engine.

    The :attr:`DataFrame.index` and
    :attr:`DataFrame.columns` attributes of the
    :class:`~pandas.DataFrame` instance are placed in the query namespace
    by default, which allows you to treat both the index and columns of the
    frame as a column in the frame.
    The identifier ``index`` is used for the frame index; you can also
    use the name of the index to identify it in a query. Please note that
    Python keywords may not be used as identifiers.

    *Backtick quoted variables*

    Backtick quoted variables are parsed as literal Python code and
    are converted internally to a Python valid identifier.
    This can lead to the following problems.

    During parsing a number of disallowed characters inside the backtick
    quoted string are replaced by strings that are allowed as a Python
    identifier.
    These characters include all operators in Python, the space character, the
    question mark, the exclamation mark, the dollar sign, and the euro sign.
    For other characters that fall outside the ASCII range (U+0001..U+007F)
    and those that are not further specified in PEP 3131,
    the query parser will raise an error.
    This excludes whitespace different than the space character,
    but also the hashtag (as it is used for comments) and the backtick
    itself (backtick can also not be escaped).

    In a special case, quotes that make a pair around a backtick can
    confuse the parser.
    For example, ```it's` > `that's``` will raise an error,
    as it forms a quoted string (``'s > `that'``) with a backtick inside.

    See also the Python documentation about lexical analysis
    (https://docs.python.org/3/reference/lexical_analysis.html)
    in combination with the source code in
    :mod:`pandas.core.computation.parsing`.

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

    pd_method = "query"


# ReplaceTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class ReplaceTF(DataFrameTF):
    """
    Replace values given in `to_replace` with `value`.

    Values of the DataFrame are replaced with other values dynamically.
    This differs from updating with ``.loc`` or ``.iloc``, which require
    you to specify a location to update with some value.

    Parameters
    ----------
    to_replace : str, regex, list, dict, Series, int, float, or None
        How to find the values that will be replaced.

        * numeric, str or regex:

            - numeric: numeric values equal to `to_replace` will be
            replaced with `value`
            - str: string exactly matching `to_replace` will be replaced
            with `value`
            - regex: regexs matching `to_replace` will be replaced with
            `value`

        * list of str, regex, or numeric:

            - First, if `to_replace` and `value` are both lists, they
            **must** be the same length.
            - Second, if ``regex=True`` then all of the strings in **both**
            lists will be interpreted as regexs otherwise they will match
            directly. This doesn't matter much for `value` since there
            are only a few possible substitution regexes you can use.
            - str, regex and numeric rules apply as above.

        * dict:

            - Dicts can be used to specify different replacement values
            for different existing values. For example,
            ``{'a': 'b', 'y': 'z'}`` replaces the value 'a' with 'b' and
            'y' with 'z'. To use a dict in this way the `value`
            parameter should be `None`.
            - For a DataFrame a dict can specify that different values
            should be replaced in different columns. For example,
            ``{'a': 1, 'b': 'z'}`` looks for the value 1 in column 'a'
            and the value 'z' in column 'b' and replaces these values
            with whatever is specified in `value`. The `value` parameter
            should not be ``None`` in this case. You can treat this as a
            special case of passing two lists except that you are
            specifying the column to search in.
            - For a DataFrame nested dictionaries, e.g.,
            ``{'a': {'b': np.nan}}``, are read as follows: look in column
            'a' for the value 'b' and replace it with NaN. The `value`
            parameter should be ``None`` to use a nested dict in this
            way. You can nest regular expressions as well. Note that
            column names (the top-level dictionary keys in a nested
            dictionary) **cannot** be regular expressions.

        * None:

            - This means that the `regex` argument must be a string,
            compiled regular expression, or list, dict, ndarray or
            Series of such elements. If `value` is also ``None`` then
            this **must** be a nested dictionary or Series.

        See the examples section for examples of each of these.
    value : scalar, dict, list, str, regex, default None
        Value to replace any values matching `to_replace` with.
        For a DataFrame a dict of values can be used to specify which
        value to use for each column (columns not in the dict will not be
        filled). Regular expressions, strings and lists or dicts of such
        objects are also allowed.
    limit : int or None, default None
        Maximum size gap to forward or backward fill.
    regex : bool or same types as `to_replace`, default False
        Whether to interpret `to_replace` and/or `value` as regular
        expressions. If this is ``True`` then `to_replace` *must* be a
        string. Alternatively, this could be a regular expression or a
        list, dict, or array of regular expressions in which case
        `to_replace` must be ``None``.
    method : {'pad', 'ffill', 'bfill', `None`}
        The method to use when for replacement, when `to_replace` is a
        scalar, list or tuple and `value` is ``None``.

    Returns
    -------
    DataFrame
        Object after replacement.

    Raises
    ------
    AssertionError
        * If `regex` is not a ``bool`` and `to_replace` is not
        ``None``.

    TypeError
        * If `to_replace` is not a scalar, array-like, ``dict``, or ``None``
        * If `to_replace` is a ``dict`` and `value` is not a ``list``,
        ``dict``, ``ndarray``, or ``Series``
        * If `to_replace` is ``None`` and `regex` is not compilable
        into a regular expression or is a list, dict, ndarray, or
        Series.
        * When replacing multiple ``bool`` or ``datetime64`` objects and
        the arguments to `to_replace` does not match the type of the
        value being replaced

    ValueError
        * If a ``list`` or an ``ndarray`` is passed to `to_replace` and
        `value` but they are not the same length.

    Notes
    -----
    `DataFrame.replace`'s `inplace` parameter is not work for transformer.
    Actually this break pipeline stream. If a transformer's `inplace` is
    `True`, the next tf input would get `None`.

    * Regex substitution is performed under the hood with ``re.sub``. The
    rules for substitution for ``re.sub`` are the same.
    * Regular expressions will only substitute on strings, meaning you
    cannot provide, for example, a regular expression matching floating
    point numbers and expect the columns in your frame that have a
    numeric dtype to be matched. However, if those floating point
    numbers *are* strings, then you can do this.
    * This method has *a lot* of options. You are encouraged to experiment
    and play with this method to gain intuition about how it works.
    * When dict is used as the `to_replace` value, it is like
    key(s) in the dict are the to_replace part and
    value(s) in the dict are the value parameter.

    Examples
    --------

    **Scalar `to_replace` and `value`**

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

    **List-like `to_replace`**

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

    **dict-like `to_replace`**

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

    **Regular expression `to_replace`**

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

    pd_method = "replace"


# SelectDtypesTF doc ported with modifications from pandas
# https://github.com/pandas-dev/pandas/blob/master/pandas/core/frame.py


class SelectDtypesTF(DataFrameTF):
    """
    Return a subset of the DataFrame's columns based on the column dtypes.

    Parameters
    ----------
    include, exclude : scalar or list-like
        A selection of dtypes or strings to be included/excluded. At least
        one of these parameters must be supplied.

    Returns
    -------
    DataFrame
        The subset of the frame including the dtypes in ``include`` and
        excluding the dtypes in ``exclude``.

    Raises
    ------
    ValueError
        * If both of ``include`` and ``exclude`` are empty
        * If ``include`` and ``exclude`` have overlapping elements
        * If any kind of string dtype is passed in.

    Notes
    -----
    * To select all *numeric* types, use ``np.number`` or ``'number'``
    * To select strings you must use the ``object`` dtype, but note that
        this will return *all* object dtype columns
    * See the `numpy dtype hierarchy
        <https://numpy.org/doc/stable/reference/arrays.scalars.html>`__
    * To select datetimes, use ``np.datetime64``, ``'datetime'`` or
        ``'datetime64'``
    * To select timedeltas, use ``np.timedelta64``, ``'timedelta'`` or
        ``'timedelta64'``
    * To select Pandas categorical dtypes, use ``'category'``
    * To select Pandas datetimetz dtypes, use ``'datetimetz'`` (new in
        0.20.0) or ``'datetime64[ns, tz]'``

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

    pd_method = "select_dtypes"
