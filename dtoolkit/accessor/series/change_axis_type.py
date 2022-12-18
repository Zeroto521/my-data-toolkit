import pandas as pd
from pandas.util._decorators import doc

from dtoolkit._typing import Axis
from dtoolkit.accessor.register import register_series_method


@register_series_method
@doc(alias="s", klass="Series")
def change_axis_type(s: pd.Series, dtype: type, axis: Axis = 0) -> pd.Series:
    """
    Change the type of the axis.

    A sugary syntax wraps :meth:`~pandas.Series.astype`::

        if axis == 0:
            {alias}.index = {alias}.index.astype(dtype)
        else:
            {alias}.columns = {alias}.columns.astype(dtype)

    Parameters
    ----------
    dtype : type
        The type to convert to.

    axis : {{0 or 'index', 1 or 'columns'}}, default 0
        The axis to convert. For Series, always convert index type.

        * 0, or 'index' : Convert index type.
        * 1, or 'columns' : Convert columns type.

    Returns
    -------
    {klass}

    See Also
    --------
    pandas.{klass}.astype
    dtoolkit.accessor.series.change_axis_type
    dtoolkit.accessor.dataframe.change_axis_type

    Examples
    --------
    >>> import dtoolkit
    >>> import pandas as pd

    Convert Series's index type from int to str:

    >>> s = pd.Series(["a", "b"])
    >>> s
    0    a
    1    b
    dtype: object
    >>> s.index
    RangeIndex(start=0, stop=2, step=1)
    >>> s.change_axis_type(str).index
    Index(['0', '1'], dtype='object')

    Convert DataFrame's index type from int to str:

    >>> df = pd.DataFrame([[1, 2], [3, 4]])
    >>> df
       0  1
    0  1  2
    1  3  4
    >>> df.index
    RangeIndex(start=0, stop=2, step=1)
    >>> df.change_axis_type(str).index
    Index(['0', '1'], dtype='object')

    Convert DataFrame's columns type from str to int:

    >>> df.columns
    RangeIndex(start=0, stop=2, step=1)
    >>> df.change_axis_type(str, axis=1).columns
    Index(['0', '1'], dtype='object')
    """

    s = s.copy()  # Avoid mutating the original Series
    s.index = s.index.astype(dtype)

    return s
