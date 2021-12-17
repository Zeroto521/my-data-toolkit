from warnings import warn

from dtoolkit.geoaccessor.tool.buffer import geographic_buffer  # noqa

warn(
    "Method 'dtoolkit.geoaccessor.tool.geographic_buffer' is deprecated "
    "and will be removed in 0.0.8. Please use "
    "'dtoolkit.geoaccessor.geoseries.geobuffer' instead. "
    "(Warning added DToolKit 0.0.7)",
    DeprecationWarning,
)
