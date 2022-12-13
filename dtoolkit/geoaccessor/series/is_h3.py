import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def is_h3(s: pd.Series, /) -> bool:
    """
    Validate whether the whole series is H3 cell index.

    Returns
    -------
    bool
        True if the whole series is H3 cell index else False.

    See Also
    --------
    h3.h3_is_valid
    """
    from h3.api.numpy_int import h3_is_valid

    return s.apply(h3_is_valid).all()
