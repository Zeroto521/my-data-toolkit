from warnings import warn

import numpy as np
import pandas as pd
from pandas.api.types import is_array_like

from dtoolkit._typing import Axis
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
        axis = df._get_axis_number(axis)
        if (
            align
            and isinstance(other, (pd.Series, pd.DataFrame))
            and not df.index.equals(other.index)
        ):
            warn("The indices are different.", stacklevel=find_stack_level())
            df, other = df.align(other, axis=1 - axis)

        if len(shape_other := np.shape(other)) == 1:
            if shape_other[0] != df.shape[1 - axis]:
                raise ValueError(
                    f"size of other ({shape_other[0]}) does not equal to df.shape"
                    f"[{1-axis}] ({df.shape[1 - axis]})."
                )

            if axis == 1:
                other = np.asarray(other).reshape((-1, 1))

    return np.equal(df, other, **kwargs)
