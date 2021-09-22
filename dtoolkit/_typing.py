from typing import Union

import pandas as pd

SeriesOrFrame = Union[pd.Series, pd.DataFrame]

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
