from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

__description__ = (
    "A series of toolkits to decrease the same work "
    "include geographic calculation, data engineering, and so on."
)
__license__ = "MIT"
