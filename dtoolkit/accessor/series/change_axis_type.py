from dtoolkit._typing import Axis
from dtoolkit.accessor.register import register_series_method


@register_series_method
def change_axis_type(s: pd.Series, dtype: type, axis: Axis = 0) -> pd.Series:

    s = s.copy()  # Avoid mutating the original Serie
    s.index = s.index.astype(dtype)

    return s
