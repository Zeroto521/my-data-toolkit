import pytest

from dtoolkit.util._decorator import deprecated_alias


@pytest.mark.parametrize(
    "args, kwargs, aliases",
    [
        ((0,), {}, {"a": "alpha"}),
        ((), {"alpha": "string"}, {"a": "alpha"}),
        ((1.0,), {"beta": "string"}, {"b": "beta"}),
        ((None,), {"beta": 0}, {"a": "alpha", "b": "beta"}),
    ],
)
def test_work(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return {"alpha": alpha, "beta": beta}

    result = func(*args, **kwargs)
    assert result["alpha"] in args or result["alpha"] == kwargs.get("alpha")
    assert result["beta"] == kwargs.get("beta")


@pytest.mark.parametrize(
    "args, kwargs, aliases",
    [
        ((), {"a": 1}, {"a": "alpha"}),
        ((0.0,), {"b": "beta"}, {"b": "beta"}),
        ((), {"a": None, "b": None}, {"a": "alpha", "b": "beta"}),
        ((), {"a": 1}, {"a": "alpha", "b": "beta"}),
        ((1,), {"b": 1}, {"a": "alpha", "b": "beta"}),
    ],
)
def test_warning(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return {"alpha": alpha, "beta": beta}

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
        ((), {"a": 1, "alpha": 2}, {"a": "alpha"}),
        ((), {"a": 1, "alpha": 1}, {"a": "alpha"}),
        ((1,), {"b": 1, "beta": 1}, {"b": "beta"}),
        ((1,), {"b": 1, "beta": 2}, {"b": "beta"}),
        ((), {"a": 1, "alpha": 2}, {"a": "alpha", "b": "beta"}),
        ((1,), {"b": 1, "beta": 1}, {"a": "alpha", "b": "beta"}),
        ((), {"a": 1, "alpha": 2, "b": 1, "beta": 1}, {"a": "alpha", "b": "beta"}),
    ],
)
def test_error(args, kwargs, aliases):
    @deprecated_alias(**aliases)
    def func(alpha, beta=None):
        return {"alpha": alpha, "beta": beta}

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
