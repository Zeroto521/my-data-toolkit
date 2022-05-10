from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method

if TYPE_CHECKING:
    from sklearn.base import TransformerMixin

    from dtoolkit._typing import IntOrStr


@register_dataframe_method
def fit_transform(
    df: pd.DataFrame,
    method: TransformerMixin,
    X: IntOrStr | list[IntOrStr] | pd.Index,
    y: IntOrStr = None,
    drop: bool = False,
    *args,
    **kwargs,
) -> pd.DataFrame:
    return (
        pd.DataFrame(
            method(*args, **kwargs).fit_transform(df[X], y=df.get(y)),
            index=df.index,
            columns=_check_feature_names_in(X),
        )
        .combine_first(
            df.drop_or_not(
                drop=drop,
                columns=X,
            ),
        )
    )
