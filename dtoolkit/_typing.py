from typing import Union

import pandas as pd

SeriesOrFrame = Union[pd.Series, pd.DataFrame]

#
# typing compat
#

try:
    # this function new in 3.8
    from typing import get_args

except ImportError:

    def get_args(tp) -> tuple:
        return tp.__args__
