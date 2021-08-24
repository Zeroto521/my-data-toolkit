from functools import wraps

from .._checking import check_dataframe_type


def require_dataframe_type(class_method):
    @wraps(class_method)
    def decorator(*args, **kwargs):
        check_dataframe_type(args[1])
        return class_method(*args, **kwargs)

    return decorator
