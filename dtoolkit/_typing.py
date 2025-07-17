from typing import Literal

import numpy as np
import pandas as pd


SeriesOrFrame = pd.Series | pd.DataFrame

TwoDimArray = np.ndarray | pd.DataFrame
OneDimArray = np.ndarray | pd.Series

Number = int | float

Axis = Literal[0, 1, "index", "columns"]  # only for dataframe axis
