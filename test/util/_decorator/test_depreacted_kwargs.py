import pytest

from dtoolkit.util._decorator import deprecated_kwargs


@pytest.mark.parametrize(
    "arguments, kwargs",
    [
        (["a"], dict(a=1)),
        (["b"], dict(b=2)),
        (["a", "b"], dict(a=1, b=2)),
        (["b", "a"], dict(a=1, b=2)),
    ],
)
def test_arguments(arguments, kwargs):
    @deprecated_kwargs(*arguments)
    def simple_sum(alpha, beta, a=0, b=0):
        return alpha + beta

    with pytest.warns(DeprecationWarning):
        simple_sum(1, 2, **kwargs)


@pytest.mark.parametrize(
    "arguments, args, excepted",
    [
        (["a"], [0, 0], 0),
        (["b"], [1, 1], 2),
        (["a", "b"], [0, 1], 1),
        (["b", "a"], [0, 1], 1),
    ],
)
def test_work(arguments, args, excepted):
    @deprecated_kwargs(*arguments)
    def simple_sum(alpha, beta, a=0, b=0):
        return alpha + beta

    assert simple_sum(*args) == excepted
