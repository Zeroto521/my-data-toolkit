from typing import Union

import numpy as np
import pandas as pd

SeriesOrFrame = Union[pd.Series, pd.DataFrame]

TwoDimArray = Union[np.ndarray, pd.DataFrame]
OneDimArray = Union[np.ndarray, pd.Series]

#
# typing.get_args compat
#

try:
    # this function new in 3.8
    from typing import get_args

except ImportError:

    def get_args(tp) -> tuple:
        """Get type arguments with all substitutions performed."""

        return tp.__args__
