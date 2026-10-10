import dtoolkit.accessor  # noqa: F401

from importlib.metadata import PackageNotFoundError, version

try:
    from ._version import __version__
except ImportError:
    try:
        __version__ = version("my-data-toolkit")
    except PackageNotFoundError:
        __version__ = "unknown"
