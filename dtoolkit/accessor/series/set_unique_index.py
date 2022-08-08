from warnings import warn

import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_series_method


@register_series_method
@doc(klass="Series", alias="s")
def set_unique_index(s: pd.Series, /, **kwargs) -> pd.Series:
    """
    Set unique index via :meth:`~pandas.{klass}.reset_index` if ``{alias}.index``
    isn't unique.

    Parameters
    ----------
     **kwargs
        See the documentation for :meth:`~pandas.{klass}.reset_index` for complete
        details on the keyword arguments.

    Returns
    -------
    {klass}

    Warns
    -----
    UserWarning
        If the index of the inputting is not unique.

    See Also
    --------
    pandas.Series.reset_index
    pandas.DataFrame.reset_index
    dtoolkit.accessor.series.set_unique_index
    dtoolkit.accessor.dataframe.set_unique_index

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> df = pd.DataFrame({{'a': [1, 2, 3], 'b': [4, 5, 6]}}, index=[0, 0, 1])
    >>> df
       a  b
    0  1  4
    0  2  5
    1  3  6

    If the index of the inputting is not unique, then it will be reset.
    And give a warning like below::

        UserWarning: The index of 'DataFrame' is not unique.

    >>> df.set_unique_index(drop=True)
       a  b
    0  1  4
    1  2  5
    2  3  6
    """

    if not s.index.is_unique:
        warn(
            f"The 'Index' of {type(s).__name__!r} is not unique.",
            stacklevel=3,
        )
        return s.reset_index(**kwargs)

    return s
