from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from .base import MethodAccessor
from .base import register_method_factory


def register_method_factory(register_accessor: callable) -> callable:

    # based on pandas_flavor/register.py
    def register_accessor_method(method: callable) -> callable:
        """
        Register a function as a method attached to the
        :obj:`~pandas.DataFrame` or :obj:`~pandas.Series`.
        """

        @register_accessor(method.__name__)
        class InnerAccessor(MethodAccessor):
            amethod = method

        # Must return method itself, otherwise would get None.
        return method

    return register_accessor_method


register_dataframe_method = register_method_factory(
    register_dataframe_accessor,
)
register_series_method = register_method_factory(
    register_series_accessor,
)
