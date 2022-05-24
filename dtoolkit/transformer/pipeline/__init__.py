from warnings import warn

from dtoolkit.transformer.pipeline.FeatureUnion import FeatureUnion  # noqa
from dtoolkit.transformer.pipeline.make_pipeline import make_pipeline  # noqa
from dtoolkit.transformer.pipeline.make_union import make_union  # noqa
from dtoolkit.transformer.pipeline.Pipeline import Pipeline  # noqa
from dtoolkit.util._exception import find_stack_level

warn(
    "The 'dtoolkit.transformer.pipeline' package will be moved into "
    "'dtoolkit.pipeline' in 0.0.17. (Warning added DToolKit 0.0.16)",
    FutureWarning,
    find_stack_level(),
)
