from typing import Union

import numpy as np
import pandas as pd

SeriesOrFrame = Union[pd.Series, pd.DataFrame]

TwoDimArray = Union[np.ndarray, pd.DataFrame]
OneDimArray = Union[np.ndarray, pd.Series]

Number = Union[int, float]

IntOrStr = Union[int, str]  # for axis or column name
Axis = Literal[0, 1, "index", "columns"]  # only for dataframe axis
