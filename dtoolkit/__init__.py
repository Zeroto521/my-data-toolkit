from importlib.metadata import PackageNotFoundError, version

import dtoolkit.accessor  # noqa: F401

try:
    from dtoolkit._version import __version__
except ImportError:
    try:
        __version__ = version("my-data-toolkit")
    except PackageNotFoundError:
        __version__ = "unknown"
