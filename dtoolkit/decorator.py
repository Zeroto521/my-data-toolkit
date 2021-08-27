from __future__ import annotations

from functools import wraps

from ._checking import check_dataframe_type
from .util import fargs_dict


def require_type_factory(check: callable):
    """Transform a checking var type function to a checking decorator."""

    @wraps(check)
    def require_type(var: str):
        def wrapper(method):
            @wraps(method)
            def decorator(*args, **kwargs):
                check_args = fargs_dict(method, *args, **kwargs)
                check(check_args.get(var, None))

                return method(*args, **kwargs)

            return decorator

        return wrapper

    return require_type


require_dataframe_type = require_type_factory(check_dataframe_type)
