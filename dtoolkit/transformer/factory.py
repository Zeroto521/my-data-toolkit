from __future__ import annotations

from inspect import isfunction

from ._util import snake_to_camel
from .base import MethodTF


def methodtf_factory(
    transform_method: callable,
    inverse_transform_method: callable | None = None,
    baseclass: MethodTF = MethodTF,
) -> MethodTF:
    """
    Quickly generate a transformer from a method.

    Parameters
    ----------
    transform_method
    inverse_transform_method
    baseclass

    Examples
    --------
    ...
    """

    if not isfunction(transform_method):
        raise TypeError("transform_method must be a function.")

    if isfunction(inverse_transform_method):
        inverse_transform_method = staticmethod(inverse_transform_method)
    elif inverse_transform_method is not None:
        raise TypeError("inverse_transform_method must be a function.")

    classname = snake_to_camel(transform_method.__name__) + "TF"

    return type(
        classname,
        (baseclass,),
        dict(
            transform_method=staticmethod(transform_method),
            inverse_transform_method=inverse_transform_method,
        ),
    )
