(how-to-build-transformer)=
# How to Build Transformer

## Generate Transformer from Method

:::{tip}
You can {download}`Download the source code for the following <../../../example/transformer/plustf.py>`.
:::

```{code-block} python
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
```

## Build {obj}`~pandas.DataFrame` Transformer

Port {obj}`~pandas.DataFrame`'s method to transformer.

```{code-block} python
from dtoolkit.transformer import DataFrameTF

class MyTF(DataFrameTF):
    """Doc here"""

    transform_method = staticmethod("DataFrame's inner method")
```

## Build {obj}`~numpy` Transformer

Port {obj}`numpy`'s method to transformer.

```{code-block} python
from dtoolkit.transformer import NumpyTF

class MyTF(NumpyTF):
    """Doc here"""

    transform_method = staticmethod("numpy's inner method")
```
