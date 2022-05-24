from __future__ import annotations

from sklearn.pipeline import _name_estimators

from dtoolkit.transformer import Transformer
from dtoolkit.transformer.pipeline.Pipeline import Pipeline


def make_pipeline(
    *steps: list[Transformer],
    memory=None,
    verbose: bool = False,
) -> Pipeline:
    """
    Construct a :class:`Pipeline` from the given estimators.

    This is a shorthand for the :class:`Pipeline` constructor; it does not
    require, and does not permit, naming the estimators. Instead, their names
    will be set to the lowercase of their types automatically.

    See Also
    --------
    Pipeline : Class for creating a pipeline of transforms with a final
        estimator.

    Examples
    --------
    >>> from sklearn.naive_bayes import GaussianNB
    >>> from sklearn.preprocessing import StandardScaler
    >>> from dtoolkit.transformer import make_pipeline
    >>> make_pipeline(StandardScaler(), GaussianNB(priors=None))
    Pipeline(steps=[('standardscaler', StandardScaler()),
                    ('gaussiannb', GaussianNB())])
    """

    return Pipeline(_name_estimators(steps), memory=memory, verbose=verbose)
