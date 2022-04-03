import pytest

from dtoolkit._decorator import warning


@pytest.mark.parametrize(
    "args, kwargs, message, exception",
    [
        ((), {}, "Nothing", None),
        ((), {}, "Nothing", UserWarning),
        ((), {}, "Nothing", FutureWarning),
        ((), {}, "Nothing", DeprecationWarning),
        ((1, 2, 3), {}, "Nothing", None),
        ((), {"a": 1, "b": 2, "c": 3}, "Nothing", None),
        ((1, 2, 3), {"a": 1, "b": 2, "c": 3}, "Nothing", None),
    ],
)
def test_work(args, kwargs, message, exception):
    @warning(message, exception)
    def func(*args, **kwargs):
        return dict(args=args, kwargs=kwargs)

    with pytest.warns(exception, match=message):
        result = func(*args, **kwargs)

    assert isinstance(result, dict)
    assert result["args"] == args
    assert result["kwargs"] == kwargs
