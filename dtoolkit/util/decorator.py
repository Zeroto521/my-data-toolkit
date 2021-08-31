def wraps(wrapped):
    """
    Keep the same additional attributes with ``wrapped``.

    Can't use :meth:`functools.wraps`, specially when ``wrapped`` type is
    :keyword:`function` and ``wrapper`` is :keyword:`class`.
    """

    def decorator(wrapper):
        wrapper.__module__ = wrapped.__module__
        wrapper.__name__ = wrapped.__name__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__qualname__ = wrapped.__qualname__
        wrapper.__annotations__ = wrapped.__annotations__

        return wrapper

    return decorator
