import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.accessor.series import s_set_unique_index


@register_dataframe_method
@doc(klass="DataFrame", alias="df")
def set_unique_index(df: pd.DataFrame, /, **kwargs) -> pd.DataFrame:
    return s_set_unique_index(df, **kwargs)
