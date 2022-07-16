import pandas as pd

from dtoolkit.accessor.register import register_series_method


@register_series_method
def query(s: pd.Series, /, expr: str, **kwargs):
    if not isinstance(expr, str):
        raise ValueError(
            f"expr must be a string to be evaluated, {type(expr)} given",
        )

    kwargs["level"] = kwargs.pop("level", 0) + 1
    kwargs["target"] = None
    mask = s.eval(expr, **kwargs)

    try:
        result = s.loc[mask]
    except ValueError:
        # when mask is multi-dimensional loc raises, but this is sometimes a
        # valid query
        result = s[mask]

    return result
