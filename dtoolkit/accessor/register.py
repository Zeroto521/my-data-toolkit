from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor
from pandas.util._decorators import doc

if TYPE_CHECKING:
    from typing import Callable

    from dtoolkit._typing import SeriesOrFrame


def register_method_factory(register_accessor):
    """
    Decrease the same things via factory pattern.

    See Also
    --------
    register_series_method
    register_dataframe_method
    dtoolkit.geoaccessor.register_geoseries_method
    dtoolkit.geoaccessor.register_geodataframe_method
    """

    # based on pandas_flavor/register.py
    def register_accessor_attr(attr: Callable | type, name: str):
        hooked_attr = attr

        if not isinstance(attr, type):  # function type

            @wraps(attr)
            def hooked_attr(pd_obj: SeriesOrFrame):
                @wraps(attr)
                def wrapper(*args, **kwargs):
                    return attr(pd_obj, *args, **kwargs)

                return wrapper

        # Register attr as pandas object inner attr.
        register_accessor(name)(hooked_attr)

        # Must return attr itself, otherwise would get None.
        return attr

    @wraps(register_accessor)
    def register_accessor_alias(name: str | None = None):
        @wraps(register_accessor)
        def wrapper(attr: Callable):
            return register_accessor_attr(attr, name or attr.__name__)

        return wrapper

    @wraps(register_accessor)
    def decorator(name: Callable | type | str | None = None):

        # Supports `@register_*_method` using.
        if callable(name) or isinstance(name, type):
            attr = name  # This 'name' variable actually is a function or class.
            return register_accessor_attr(attr, attr.__name__)

        # Supports `@register_*_method()` and `@register_*_method(name="")` using.
        return register_accessor_alias(name)

    return decorator


@register_method_factory
@doc(klass=":class:`~pandas.Series`")
def register_series_method(name: str | None = None):
    """
    {klass} register accessor for human.

    Write method normally, use method naturally.

    Parameters
    ----------
    name : str, optional
        Use the ``method`` name as the default accessor entrance if ``name`` is None.

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

        @register_dataframe_method(name="col")
        @register_series_method(name="col")  # Support alias name also.
        @register_dataframe_method
        @register_series_method  # Use accessor method `__name__` as the entrance.
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

        In [5]: df.col()
        Out[5]:
        ['a', 'b']

        In [6]: df.a.col()
        Out[6]:
        'a'
    """
    return register_series_accessor(name)


@register_method_factory
@doc(register_series_method, klass=":class:`~pandas.DataFrame`")
def register_dataframe_method(name: str | None = None):
    return register_dataframe_accessor(name)
