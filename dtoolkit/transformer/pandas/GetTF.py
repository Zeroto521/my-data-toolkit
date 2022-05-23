import pandas as pd

from dtoolkit.transformer.base import DataFrameTF


class GetTF(DataFrameTF):
    """
    A transformer could get item from object for given key
    (ex: :obj:`~pandas.DataFrame` column).

    See Also
    --------
    pandas.DataFrame.get : This transformer's prototype method.
    """

    transform_method = staticmethod(pd.DataFrame.get)
