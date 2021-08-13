(how-to-build-transformer)=
# How to Build Transformer

## Build {obj}`~pandas.DataFrame` Transformer

Port DataFrame's function to transformer.

```{code-block} python
from dtoolkit.transformer import DataFrameTF

class MyTF(DataFrameTF):
    """Doc here"""

    pd_method = "DataFrameMethod"
```

:::{note}
`pd_method` should be `DataFrame`'s method.
The following codes show how the method work.

```{code-block} python
getattr(X, self.pd_method)(*args, **kwargs)
```
:::

## Build {obj}`~numpy` Transformer

Port `numpy`'s function to transformer.

```{code-block} python
from dtoolkit.transformer import NumpyTF

class MyTF(DataFrameTF):
    """Doc here"""

    np_method = "NumpyMethod"
```

:::{note}
`np_method` should be `numpy`'s method.
The following codes show how the method work.

```{code-block} python
getattr(numpy, self.np_method)(*args, **kwargs)
```
:::
