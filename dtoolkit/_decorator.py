from functools import wraps
from warnings import warn


def warning(message: str, category: Exception = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warn(message, category=category)

            return func(*args, **kwargs)

        return wrapper

    return decorator
