import pandas as pd

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import set_unique_index as s_set_unique_index
from dtoolkit.util._decorator import doc


@register_dataframe_method
@doc(s_set_unique_index, klass="DataFrame", alias="df")
def set_unique_index(df: pd.DataFrame, /, **kwargs) -> pd.DataFrame:
    return s_set_unique_index(df, **kwargs)
