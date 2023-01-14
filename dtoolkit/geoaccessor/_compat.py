from packaging.version import Version


# -----------------------------------------------------------------------------
# h3 compat
# -----------------------------------------------------------------------------

try:
    from h3 import __version__ as h3_version

    H3_GE_4 = Version(h3_version) >= Version("4.0.0a")

except ImportError:

    H3_GE_4 = None


def h3_3or4(v3: str, v4: str) -> str:
    """Choice h3 method based on version."""

    return v4 if H3_GE_4 else v3
