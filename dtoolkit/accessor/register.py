from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor
from pandas.util._decorators import doc

if TYPE_CHECKING:
    from dtoolkit._typing import SeriesOrFrame


def register_method_factory(register_accessor):
    """
    Decrease the same things via factory pattern.

    See Also
    --------
    register_series_method
    register_dataframe_method
    """

    # based on pandas_flavor/register.py
    @wraps(register_accessor)
    def register_accessor_method(method):
        @wraps(method)
        def method_accessor(pd_obj: SeriesOrFrame):
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(pd_obj, *args, **kwargs)

            return wrapper

        register_accessor(method.__name__)(method_accessor)

        # Must return method itself, otherwise would get None.
        return method

    return register_accessor_method


@register_method_factory
@doc(klass=":class:`pandas.Series`")
def register_series_method(method):
    """
    {klass} register accessor for human.

    Write method normally, use method naturally.

    See Also
    --------
    register_series_method
    register_dataframe_method
    pandas.api.extensions.register_series_accessor
    pandas.api.extensions.register_dataframe_accessor

    Examples
    --------
    In your library code::

        import pandas as pd

        @register_dataframe_method
        @register_series_method
        def cols(pd_obj):
            '''
            An API to gather :attr:`~pandas.Series.name` and
            :attr:`~pandas.DataFrame.columns` to one.
            '''
            if isinstance(pd_obj, pd.Series):
                return pd_obj.name

            return pd_obj.columns.tolist()

    Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: import pandas as pd

        In [2]: df = pd.DataFrame({{"a": [1, 2], "b": [3, 4]}})

        In [3]: df.cols()
        Out[3]:
        ['a', 'b']

        In [4]: df.a.cols()
        Out[4]:
        'a'
    """
    return register_series_accessor(method)


@register_method_factory
@doc(register_series_method, klass=":class:`pandas.DataFrame`")
def register_dataframe_method(method):
    return register_dataframe_accessor(method)
