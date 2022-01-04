from __future__ import annotations

from typing import TYPE_CHECKING

from dtoolkit.transformer.base import MethodTF
from dtoolkit.util.generic import snake_to_camel

if TYPE_CHECKING:
    from typing import Callable


def methodtf_factory(
    transform_method: Callable,
    inverse_transform_method: Callable | None = None,
) -> MethodTF:
    """
    Quickly generate transformer from methods.

    Parameters
    ----------
    transform_method : Callable
        The back algorithm of the :func:`~MethodTF.transform`.
    inverse_transform_method : Callable or None
        The back algorithm of the :func:`~MethodTF.inverse_transform`.

    Examples
    --------
    In your library code::

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


    Back in an interactive IPython session, use this transformer:

    .. code-block:: ipython

        In [1]: import numpy as np

        In [2]: a = np.array([1, 2, 3])

        In [3]: tf = PlusTF(1).update_invargs(1)

        In [4]: tf.transform(a)
        Out[4]:
        [2 3 4]

        In [5]: tf.inverse_transform(a)
        Out[5]:
        [0 1 2]
    """

    if not callable(transform_method):
        raise TypeError("'transform_method' must be a function.")

    if (inverse_transform_method is not None) and (
        not callable(inverse_transform_method)
    ):
        raise TypeError("'inverse_transform_method' must be a function.")

    classname = snake_to_camel(transform_method.__name__) + "TF"

    return type(
        classname,
        (MethodTF,),
        dict(
            transform_method=staticmethod(transform_method),
            inverse_transform_method=staticmethod(inverse_transform_method),
        ),
    )
