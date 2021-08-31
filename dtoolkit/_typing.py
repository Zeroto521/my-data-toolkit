from typing import Union

from pandas import DataFrame
from pandas import Series

PandasTypeList = [Series, DataFrame]
PandasType = Union[tuple(PandasTypeList)]
