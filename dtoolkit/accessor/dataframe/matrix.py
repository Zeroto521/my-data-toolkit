from dataclasses import dataclass
from functools import wraps
from typing import Hashable

import pandas as pd
from pandas.api.extensions import register_dataframe_accessor


def available_if(check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check(args[0]):
                raise TypeError(
                    "Because of `df.shape[0] != df.shape[1]`, "
                    f"the '.matrix.{func.__name__}' is not available."
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_dataframe_accessor("matrix")
@dataclass
class Matrix:
    df: pd.DataFrame

    @property
    def is_valid(self) -> bool:
        return self.df.shape[0] == self.df.shape[1]

    def to_table(
        self,
        index: Hashable = "index",
        columns: Hashable = "columns",
        values: Hashable = "values",
    ) -> pd.DataFrame:
        """
        Transform matrix to table.

        Parameters
        ----------
        index : Hashable, default 'index'
            The name of index. If ``.index.name`` is not None, use it first.

        columns : Hashable, default 'columns'
            The name of columns. If ``.columns.name`` is not None, use it first.

        values : Hashable, default 'values'
            The name of values.

        Examples
        --------
        >>> import dtoolkit.accessor
        >>> import pandas as pd
        >>> df = pd.DataFrame([[1, 2, 3], [2, 1, 3], [3, 2, 1]])
        >>> df
           0  1  2
        0  1  2  3
        1  2  1  3
        2  3  2  1
        >>> df.matrix.to_table()
           index  column  value
        0      0       0      1
        1      0       1      2
        2      0       2      3
        3      1       0      2
        4      1       1      1
        5      1       2      3
        6      2       0      3
        7      2       1      2
        8      2       2      1
        """

        # TODO: `drop_self`: index == column
        # TODO: `drop_duplicates`: 0-1 and 1-0
        return (
            self.df.stack()
            .rename(values)
            .rename_axis(
                (
                    self.df.index.name or index,
                    self.df.columns.name or columns,
                )
            )
            .reset_index()
        )
