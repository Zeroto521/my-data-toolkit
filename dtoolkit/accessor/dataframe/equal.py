from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_array_like

from dtookit._typing import Axis
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.util._exception import find_stack_level


@register_dataframe_method
def equal(
    df: pd.DataFrame,
    /,
    other,
    align: bool = True,
    axis: Axis = 0,
    **kwargs,
) -> pd.DataFrame:
    if is_array_like(other):
        if align and isinstance(other, pd.Series) and not df.index.equals(other.index):
            # FIXME: Wether check DataFrame's index.
            # And use `.align` will change the values of `df`.
            warn("The indices are different.", stacklevel=find_stack_level())
            df, other = df.align(other)

        if pd.DataFrame._get_axis_number(axis) == 1 and len(np.shape(other)) == 1:
            # TODO: Do something to other, reshape it ot (n, 1)
            ...

    return np.equal(df, other, **kwargs)
