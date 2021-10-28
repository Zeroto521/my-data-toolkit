from __future__ import annotations

from functools import wraps

from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from dtoolkit._typing import SeriesOrFrame


def register_method_factory(register_accessor):
    """
    Decrease the same things via factory pattern.
    """

    # based on pandas_flavor/register.py
    def register_accessor_method(method):
        """
        Register a function as a pandas's object native method.

        See Also
        --------
        register_series_method
        register_dataframe_method
        pandas.api.extensions.register_series_accessor
        pandas.api.extensions.register_dataframe_accessor

        Examples
        --------
        In your library code::

            @register_dataframe_method
            @register_series_method
            def cols(pd_obj):
                '''
                A API to gather :attr:`~pandas.Series.name` and
                :attr:`~pandas.DataFrame.columns` to one.
                '''
                if isinstance(pd_obj, pd.Series):
                    return pd_obj.name

                return pd_obj.columns.tolist()

        Back in an interactive IPython session:

            .. ipython::

                In [1]: import pandas as pd

                In [2]: df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

                In [3]: df.cols()
                Out[3]: ['a', 'b']

                In [4]: df.a.cols()
                Out[4]: 'a'
        """

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
def register_series_method(method):
    return register_series_accessor(method)


@register_method_factory
def register_dataframe_method(method):
    return register_dataframe_accessor(method)
