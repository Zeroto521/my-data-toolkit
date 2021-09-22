from __future__ import annotations

from functools import wraps
from inspect import isfunction

from ..util.generic import snake_to_camel
from .base import MethodTF


def methodtf_factory(
    transform_method: callable,
    inverse_transform_method: callable | None = None,
) -> MethodTF:
    """
    Quickly generate transformer from methods.

    Parameters
    ----------
    transform_method : callable
        The back algorithm of the :func:`~MethodTF.transform`.
    inverse_transform_method : callable or None
        The back algorithm of the :func:`~MethodTF.inverse_transform`.

    Examples
    --------

    .. code-block:: python

        from __future__ import annotations

        import numpy as np

        from dtoolkit.transformer.factory import methodtf_factory


        # Generate a plus/minus constant transformer:


        def plus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
            '''Plus constant to each element of ``X``'''

            return X + constant


        def minus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
            '''Minus constant to each element of ``X``'''

            return X - constant


        PlusTF = methodtf_factory(plus_constant, minus_constant)


        # Use this transformer:

        a = np.array([1, 2, 3])
        tf = PlusTF(1).update_invargs(1)
        tf.transform(a)
        # [2 3 4]
        tf.inverse_transform(a)
        # [0 1 2]
    """

    if not isfunction(transform_method):
        raise TypeError("transform_method must be a function.")
    else:
        transform_method = wraps(transform_method)(
            staticmethod(transform_method),
        )

    if isfunction(inverse_transform_method):
        inverse_transform_method = wraps(inverse_transform_method)(
            staticmethod(inverse_transform_method),
        )
    elif inverse_transform_method is not None:
        raise TypeError("inverse_transform_method must be a function.")

    classname = snake_to_camel(transform_method.__name__) + "TF"

    return type(
        classname,
        (MethodTF,),
        dict(
            transform_method=transform_method,
            inverse_transform_method=inverse_transform_method,
        ),
    )
