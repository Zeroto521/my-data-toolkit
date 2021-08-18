from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from .base import Accessor


def register_method_factory(register_accessor: callable) -> callable:

    # based on pandas_flavor/register.py
    def register_accessor_method(method: callable) -> callable:
        """
        Register a function as a method attached to the
        :obj:`~pandas.DataFrame` or :obj:`~pandas.Series`.
        """

        @register_accessor(method.__name__)
        class InnerAccessor(Accessor):
            __module__ = method.__module__
            __name__ = method.__name__
            __doc__ = method.__doc__
            __qualname__ = method.__qualname__
            __annotations__ = method.__annotations__

            def __call__(self, *args, **kwargs):
                return method(self.pd_obj, *args, **kwargs)

        # Must return method itself, otherwise would get None.
        return method

    return register_accessor_method


register_dataframe_method = register_method_factory(
    register_dataframe_accessor,
)
register_series_method = register_method_factory(
    register_series_accessor,
)
