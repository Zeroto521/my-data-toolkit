from functools import wraps


def nb_speedup(method: str = "jit", /, **kwargs):
    """
    Use numba to speed up the function if numba is installed.

    Parameters
    ----------
    method : str, default "jit"
        The numba decorator to use.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            try:
                module = __import__("numba")
                func_wrapped = getattr(module, method)(func, **kwargs)
                return func_wrapped(*f_args, **f_kwargs)

            except ImportError:
                return func(*f_args, **f_kwargs)

        return wrapper

    return decorator
