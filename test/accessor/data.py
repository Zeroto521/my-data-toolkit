import numpy as np
import pandas as pd

data_size = 42
s = pd.Series(range(data_size), name="item", dtype=float)

label_size = 3
d = pd.DataFrame(
    {
        "a": np.random.randint(label_size, size=data_size),
        "b": np.random.randint(label_size, size=data_size),
    },
    dtype=float,
)
s_inf = pd.Series([np.inf, -np.inf])
