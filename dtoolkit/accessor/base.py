from .._typing import Pd


class Accessor:
    """
    :obj:`~pandas.Series` and :obj:`~pandas.DataFrame` objects base class.

    Parameters
    ----------
    pd_obj : {:obj:`~pandas.Series`, :obj:`~pandas.DataFrame`}
        pandas's object

    See Also
    --------
    pandas.api.extensions.register_series_accessor
    pandas.api.extensions.register_dataframe_accessor

    Examples
    --------
    >>> from dtoolkit.accessor.base import Accessor
    >>> from pandas.api.extensions import register_dataframe_accessor
    >>> from pandas.api.extensions import register_series_accessor

    Hook function to :obj:`~pandas.DataFrame` without any other function just
    one (ex: :func:`~pandas.DataFrame.HookingName`)

    >>> @register_series_accessor('HookingName')
    ... class MyAccessor(Accessor):
    ...     def __call__(self):
    ...         ...
    """

    def __init__(self, pd_obj: Pd):
        self.pd_obj = pd_obj
