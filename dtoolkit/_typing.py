from typing import Union

import numpy as np
import pandas as pd

SeriesOrFrame = Union[pd.Series, pd.DataFrame]

TwoDimArray = Union[np.ndarray, pd.DataFrame]
OneDimArray = Union[np.ndarray, pd.Series]
