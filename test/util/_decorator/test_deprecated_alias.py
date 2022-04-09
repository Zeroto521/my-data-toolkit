import pytest

from dtoolkit.util._decorator import deprecated_alias


@pytest.mark.parametrize(
    "args, kwargs, aliases",
    [
        ((0,), {}, dict(a="alpha")),
        ((), dict(alpha="string"), dict(a="alpha")),
        ((1.0,), dict(beta="string"), dict(b="beta")),
        ((None,), dict(beta=0), dict(a="alpha", b="beta")),
    ],
)
def test_work(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return dict(alpha=alpha, beta=beta)

    result = func(*args, **kwargs)
    assert result["alpha"] in args or result["alpha"] == kwargs.get("alpha")
    assert result["beta"] == kwargs.get("beta")


@pytest.mark.parametrize(
    "args, kwargs, aliases",
    [
        ((), dict(a=1), dict(a="alpha")),
        ((0.0,), dict(b="beta"), dict(b="beta")),
        ((), dict(a=None, b=None), dict(a="alpha", b="beta")),
        ((), dict(a=1), dict(a="alpha", b="beta")),
        ((1,), dict(b=1), dict(a="alpha", b="beta")),
    ],
)
def test_warning(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return dict(alpha=alpha, beta=beta)

    with pytest.warns(DeprecationWarning):
        result = func(*args, **kwargs)

        new_to_old_alias = {v: k for k, v in aliases.items()}

        assert (
            result["alpha"] in args
            or result["alpha"] == kwargs.get(new_to_old_alias.get("alpha"))
            or result["alpha"] == kwargs.get("alpha")
        )
        assert result["beta"] == kwargs.get("beta") or result["beta"] == kwargs.get(
            new_to_old_alias.get("beta"),
        )


@pytest.mark.parametrize(
    "args, kwargs, aliases",
    [
        ((), dict(a=1, alpha=2), dict(a="alpha")),
        ((), dict(a=1, alpha=1), dict(a="alpha")),
        ((1,), dict(b=1, beta=1), dict(b="beta")),
        ((1,), dict(b=1, beta=2), dict(b="beta")),
        ((), dict(a=1, alpha=2), dict(a="alpha", b="beta")),
        ((1,), dict(b=1, beta=1), dict(a="alpha", b="beta")),
        ((), dict(a=1, alpha=2, b=1, beta=1), dict(a="alpha", b="beta")),
    ],
)
def test_error(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return dict(alpha=alpha, beta=beta)

    with pytest.raises(TypeError):
        result = func(*args, **kwargs)

        new_to_old_alias = {v: k for k, v in aliases.items()}

        assert (
            result["alpha"] in args
            or result["alpha"] == kwargs.get(new_to_old_alias.get("alpha"))
            or result["alpha"] == kwargs.get("alpha")
        )
        assert result["beta"] == kwargs.get("beta") or result["beta"] == kwargs.get(
            new_to_old_alias.get("beta"),
        )
