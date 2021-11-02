from warnings import warn

from dtoolkit.geography.buffer import geographic_buffer
from dtoolkit.geography.coordinate import coords
from dtoolkit.geography.coordinate import coords_num
from dtoolkit.geography.coordinate import coords_numlist

warn(
    "Package 'dtoolkit.geography' is deprecated and will be removed in 0.0.5. "
    "Please use 'dtoolkit.geoaccessor' instead. (Warning added DToolKit 0.0.4)",
    DeprecationWarning,
)

__all__ = [
    "geographic_buffer",
    "coords",
    "coords_numlist",
    "coords_num",
]
