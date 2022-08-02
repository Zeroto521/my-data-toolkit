import pandas as pd
from pandas.util._decorators import doc
from warnings import warn

from dtoolkit.accessor.register import register_series_method


@register_series_method
@doc(klass="Series", alias="s")
def set_unique_index(s: pd.Series, /, **kwargs) -> pd.Series:
    """
    Set unique index via :meth:`~pandas.{klass}.reset_index`` if ``{alias}.index``
    isn't unique.

    Parameters
    ----------
     **kwargs
        See the documentation for :meth:``~pandas.{klass}.set_index`` for complete
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
    """

    if not s.index.is_unique:
        warn(
            f"The 'Index' of {type(data).__name__!r} is not unique.",
            stacklevel=3,
        )
        return s.reset_index(**kwargs)

    return s
