from packaging.version import Version
from sklearn import __version__ as sklearn_version

# -----------------------------------------------------------------------------
# scikit-learn compat
# -----------------------------------------------------------------------------

SKLEARN_GE_12 = Version(sklearn_version) >= Version("1.2.0")
