import pandas as pd

from dtoolkit.transformer import DataFrameTF


class AssignTF(DataFrameTF):
    """
    A transformer could assign new columns to a :obj:`~pandas.DataFrame`.

    See Also
    --------
    pandas.DataFrame.assign : This transformer's prototype method.

    Examples
    --------
    >>> import pandas as pd
    >>> from dtoolkit.transformer import AssignTF
    >>> df = pd.DataFrame({'temp_c': [17.0, 25.0]}, index=['Portland', 'Berkeley'])
    >>> df
                temp_c
    Portland    17.0
    Berkeley    25.0

    Where the value is a callable, evaluated on ``df``:

    >>> pipeline = AssignTF(temp_f=lambda x: x.temp_c * 9 / 5 + 32)
    >>> pipeline.transform(df)
                temp_c  temp_f
    Portland    17.0    62.6
    Berkeley    25.0    77.0
    """

    transform_method = staticmethod(pd.DataFrame.assign)
