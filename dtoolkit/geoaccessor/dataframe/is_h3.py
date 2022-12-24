import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_dataframe_method
from dtoolkit.geoaccessor.index import is_h3 as i_is_h3


@register_dataframe_method
@doc(i_is_h3, klass="Series")
def is_h3(df: pd.DataFrame, /) -> bool:

    return i_is_h3(df.index)
