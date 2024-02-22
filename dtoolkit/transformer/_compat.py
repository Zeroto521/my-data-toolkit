from packaging.version import Version
from pandas import __version__ as pandas_version


# -----------------------------------------------------------------------------
# pandas compat
# -----------------------------------------------------------------------------

PANDAS_GE_14 = Version(pandas_version) >= Version("1.4.0")
