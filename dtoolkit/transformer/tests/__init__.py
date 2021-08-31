import numpy as np
import pandas as pd
import pytest

import dtoolkit._compat as compat

need_dependency = pytest.mark.skipif(
    not compat.HAS_SKLEARN,
    reason="transformer requires `sklearn`",
)

if compat.HAS_SKLEARN:
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    feature_names = iris.feature_names
    df_iris = iris.data
    s = iris.target
    array = df_iris.values

    period_names = [f"h_{t}" for t in range(24 + 1)]
    df_period = pd.DataFrame(
        np.random.randint(
            len(period_names),
            size=(len(df_iris), len(period_names)),
        ),
        columns=period_names,
    )

    label_size = 3
    data_size = len(df_iris)
    df_label = pd.DataFrame(
        {
            "a": np.random.randint(label_size, size=data_size),
            "b": np.random.randint(label_size, size=data_size),
        },
    )

    df_mixed = pd.concat([df_iris, df_label], axis=1)
