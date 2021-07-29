import numpy as np

from .base import Transformer


class RavelTF(Transformer):
    def operate(self, *args, **kwargs):
        return np.ravel(*args, **kwargs)
