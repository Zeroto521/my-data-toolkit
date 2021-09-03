from __future__ import annotations

import pandas as pd


class Accessor:
    """
    Hook method or object into :obj:`~pandas.Series` or
    :obj:`~pandas.DataFrame`.

    Parameters
    ----------
    pd_obj : :obj:`~pandas.Series` or :obj:`~pandas.DataFrame`
        pandas's object

    See Also
    --------
    pandas.api.extensions.register_series_accessor
    pandas.api.extensions.register_dataframe_accessor
    """

    def __init__(self, pd_obj: pd.Series | pd.DataFrame):
        self.pd_obj = pd_obj
