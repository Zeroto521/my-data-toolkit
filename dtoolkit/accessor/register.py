from pandas.api.extensions import register_dataframe_accessor
from pandas.api.extensions import register_series_accessor

from ..util import wraps
from .base import Accessor


def register_method_factory(register_accessor: callable) -> callable:
    """
    Decrease the same things via factory pattern.
    """

    # based on pandas_flavor/register.py
    def register_accessor_method(method: callable) -> callable:
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
        .. code-block:: python

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

        >>> import pandas as pd
        >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        >>> df.cols()
        ['a', 'b']
        >>> df.a.cols()
        'a'
        """

        @register_accessor(method.__name__)
        @wraps(method)
        class PdCustomMethod(Accessor):
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
