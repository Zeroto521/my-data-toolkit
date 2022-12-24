import pandas as pd
from pandas.util._decorators import doc

from dtoolkit.accessor.register import register_series_method
from dtoolkit.geoaccessor.index import is_h3 as i_is_h3


@register_series_method
@doc(i_is_h3, klass="Series")
def is_h3(s: pd.Series, /) -> bool:

    return i_is_h3(s.index)
