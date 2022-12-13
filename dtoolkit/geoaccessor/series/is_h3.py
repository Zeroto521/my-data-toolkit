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
    # TODO: Use `is_valid_cell` instead of `h3_is_valid`
    # While h3-py release 4, `is_valid_cell` is not available.

    # requires h3 >= 4
    # from h3.api.numpy_int import is_valid_cell
    # requires h3 < 4
    from h3.api.numpy_int import h3_is_valid

    return s.apply(h3_is_valid).all()
