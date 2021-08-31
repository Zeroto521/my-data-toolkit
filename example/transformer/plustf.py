from __future__ import annotations

import numpy as np

from dtoolkit.transformer.factory import methodtf_factory


# Generate a plus/minus constant transformer:


def plus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
    """Plus constant to each element of ``X``"""

    return X + constant


def minus_constant(X: np.ndarray, constant: int | float) -> np.ndarray:
    """Minus constant to each element of ``X``"""

    return X - constant


PlusTF = methodtf_factory(plus_constant, minus_constant)


# Use this transformer:

a = np.array([1, 2, 3])
tf = PlusTF(constant=1).update_invargs(constant=1)
tf.transform(a)
# [2 3 4]
tf.inverse_transform(a)
# [0 1 2]
