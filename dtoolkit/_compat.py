import warnings
from importlib import import_module

from packaging.version import parse as vparse


def has_moudle(name: str, mini_version: str = "") -> bool:
    """
    Detect this module exists and meets the minimal version.

    Parameters
    ----------
    name : str
        The module name.
    mini_version : str, default ""
        The module minimal version.

    Returns
    -------
    bool
        True if the module exists and meets the minimal version.
    """

    try:
        module = import_module(name)

        module_version = module.__version__
        if vparse(module_version) >= vparse(mini_version):
            return True

        warnings.warn(
            f"The installed version of {name} is too old "
            f"({module_version} installed, {mini_version} required).",
            UserWarning,
        )
        return False

    except ImportError:
        return False


#
# geography compat
#

HAS_GEOPANDAS = has_moudle("geopandas", "0.9")

#
# transformer compat
#

HAS_SKLEARN = has_moudle("sklearn", "0.24")
HAS_ITERTOOLS = has_moudle("more_itertools", "7.1.0")
