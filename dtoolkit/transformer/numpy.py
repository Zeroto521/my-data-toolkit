import numpy as np
import pandas as pd

from .base import Transformer


class NumpyTransformer(Transformer):
    np_method: str

    def operate(self, X: pd.DataFrame, *args, **kwargs) -> np.ndarray:
        return getattr(np, self.np_method)(X, *args, **kwargs)


class RavelTF(NumpyTransformer):
    """
    A transformer could return a contiguous flattened array.

    This transformer is used to handle that sklearn model requires ``y``'s
    shape is ``(n, )``. But actually we always forget this. So you would get
    a ``DataConversionWarning`` ::

        DataConversionWarning: A column-vector y was passed when a 1d array
        was expected. Please change the shape of y to (n_samples, ), for
        example using ravel().

    See Also
    --------
    numpy.ravel : this transformer's prototype method.

    Examples
    --------
    >>> from dtoolkit.transformer import RavelTF
    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> tf = RavelTF()
    >>> tf.transform(x)
    array([1, 2, 3, 4, 5, 6])
    """

    np_method = "ravel"
