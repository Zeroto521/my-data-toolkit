import pytest

pytest.importorskip("sklearn")

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


iris = load_iris(as_frame=True)
feature_names = iris.feature_names
df_iris = iris.data
s = iris.target
array = df_iris.values

label_size = 3
data_size = len(df_iris)
df_label = pd.DataFrame(
    {
        "a": np.random.randint(label_size, size=data_size),
        "b": np.random.randint(label_size, size=data_size),
    },
)


df_mixed = pd.concat([df_iris, df_label], axis=1)
