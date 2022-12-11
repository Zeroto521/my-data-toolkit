import pandas as pd
from pandas.util._decorators import doc

from dtoolkit._typing import Axis
from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series.change_axis_type import (
    change_axis_type as s_change_axis_type,
)


@register_dataframe_method
@doc(s_change_axis_type, alias="df", klass="DataFrame")
def change_axis_type(df: pd.DataFrame, dtype: type, axis: Axis = 0) -> pd.DataFrame:
    axis = df._get_axis_number(axis)

    df = df.copy()  # Avoid mutating the original DataFrame
    if axis == 0:
        df.index = df.index.astype(dtype)
    else:
        df.columns = df.columns.astype(dtype)

    return df
