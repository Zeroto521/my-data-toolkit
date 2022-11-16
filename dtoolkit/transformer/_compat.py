from packaging.version import Version
from pandas import __version__ as pandas_version
from sklearn import __version__ as sklearn_version


# -----------------------------------------------------------------------------
# pandas compat
# -----------------------------------------------------------------------------

PANDAS_GE_14 = Version(pandas_version) >= Version("1.4.0")


# -----------------------------------------------------------------------------
# scikit-learn compat
# -----------------------------------------------------------------------------

SKLEARN_GE_12 = Version(sklearn_version) >= Version("1.2.0")
