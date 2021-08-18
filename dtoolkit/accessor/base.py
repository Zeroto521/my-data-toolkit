from __future__ import annotations

from textwrap import dedent

from pandas.util._decorators import doc

from .._typing import Pd


class Accessor:
    """
    Hook method or object into :obj:`~pandas.Series` or
    :obj:`~pandas.DataFrame`.

    Parameters
    ----------
    pd_obj : :obj:`~pandas.Series` or :obj:`~pandas.DataFrame`
        pandas's object

    See Also
    --------
    pandas.api.extensions.register_series_accessor
    pandas.api.extensions.register_dataframe_accessor
    """

    def __init__(self, pd_obj: Pd):
        self.pd_obj = pd_obj


@doc(
    Accessor,
    dedent(
        """
    Examples
    --------
    >>> from dtoolkit.accessor.base import MethodAccessor
    >>> from pandas.api.extensions import register_dataframe_accessor
    >>> from pandas.api.extensions import register_series_accessor

    Hook function to :obj:`~pandas.DataFrame` without any other function just
    one (ex: :func:`~pandas.DataFrame.HookingName`)

    >>> @register_dataframe_accessor('HookingName')
    ... class MyAccessor(MethodAccessor):
    ...     method = yourmethod
    """,
    ),
)
class MethodAccessor(Accessor):
    amethod: callable[..., Pd]

    def __call__(self, *args, **kwargs):
        return self.amethod(self.pd_obj, *args, **kwargs)
