from __future__ import annotations

from functools import wraps
from typing import Callable

from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_index_accessor
from pandas.api.extensions import register_series_accessor
from pandas.util._decorators import doc

from dtoolkit._typing import SeriesOrFrame


def register_method_factory(register_accessor, /):
    """
    Let pandas-object like accessor which only hooks class also hooks function easily.

    Read more in the `User Guide`_.

    .. _User Guide: ../../guide/tips_about_accessor.ipynb#Extend-to-Pandas-like-Object

    Parameters
    ----------
    register_accessor : Pandas-object like accessor

    See Also
    --------
    register_dataframe_method
    register_series_method
    register_index_method
    dtoolkit.geoaccessor.register_geoseries_method
    dtoolkit.geoaccessor.register_geodataframe_method
    """

    # based on pandas_flavor/register.py
    def register_accessor_method(method: Callable, name: str, /):
        @wraps(method)
        def method_accessor(pd_obj: SeriesOrFrame, /):
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(pd_obj, *args, **kwargs)

            return wrapper

        # Register method as pandas object inner method.
        register_accessor(name)(method_accessor)

        # Must return method itself, otherwise would get None.
        return method

    def register_accessor_alias(name: str = None, /):
        def wrapper(method: Callable, /):
            return register_accessor_method(method, name or method.__name__)

        return wrapper

    @wraps(register_accessor)
    def decorator(name: Callable | str = None, /):
        if callable(name):  # Supports `@register_*_method` using.
            method = name  # This 'name' variable actually is a function.
            return register_accessor_method(method, method.__name__)

        # Supports `@register_*_method()` using.
        return register_accessor_alias(name)

    return decorator


@register_method_factory
@doc(klass=":class:`~pandas.Series`")
def register_series_method(name: str = None):
    """
    {klass} register accessor for human.

    Write method normally, use method naturally.

    Read more in the `User Guide`_.

    .. _User Guide: ../../guide/tips_about_accessor.ipynb

    Parameters
    ----------
    name : str, optional
        Use the ``method`` name as the default accessor entrance if ``name`` is None.

    See Also
    --------
    register_dataframe_method
    register_series_method
    register_index_method
    pandas.api.extensions.register_dataframe_accessor
    pandas.api.extensions.register_series_accessor
    pandas.api.extensions.register_index_accessor

    Examples
    --------
    In your library code::

        from __future__ import annotations

        from dtoolkit.accessor import register_dataframe_method
        from dtoolkit.accessor import register_series_method
        from dtoolkit.accessor import register_index_method
        import pandas as pd

        @register_index_method("col")  # Support alias name also.
        @register_series_method("col")
        @register_dataframe_method("col")
        @register_index_method  # Use accessor method's `__name__` as the entrance.
        @register_series_method
        @register_dataframe_method
        def cols(pd_obj) -> int | str | list[int | str] | None:
            '''
            An API to gather :attr:`~pandas.Series.name` and
            :attr:`~pandas.DataFrame.columns` to one.
            '''

            if isinstance(pd_obj, (pd.Series, pd.Index)):
                return pd_obj.name

            return pd_obj.columns.tolist()

    Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: import pandas as pd

        In [2]: df = pd.DataFrame(
           ...:     {{
           ...:         "a": [1, 2],
           ...:         "b": [3, 4],
           ...:     }},
           ...:     index=pd.Index(
           ...:         ["x", "y"],
           ...:         name="c",
           ...:     ),
           ...: )

        In [3]: df
        Out[3]:
           a  b
        c
        x  1  3
        y  2  4

        Get the columns of DataFrame via `cols` or `col` method

        In [4]: df.col()
        Out[4]: ['a', 'b']

        Get name of Series via `cols` or `col` method

        In [5]: df.a.col()
        Out[5]: 'a'

        Get name of Index via `cols` or `col` method

        In [6]: df.index.col()
        Out[6]: 'c'
    """

    return register_series_accessor(name)


@register_method_factory
@doc(register_series_method, klass=":class:`~pandas.DataFrame`")
def register_dataframe_method(name: str = None):
    return register_dataframe_accessor(name)


@register_method_factory
@doc(register_series_method, klass=":class:`~pandas.Index`")
def register_index_method(name: str = None):
    return register_index_accessor(name)
