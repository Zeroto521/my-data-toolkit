from __future__ import annotations

import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import clone
from sklearn.pipeline import _fit_transform_one
from sklearn.pipeline import _name_estimators
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.pipeline import Pipeline as SKPipeline
from sklearn.utils import _print_elapsed_time
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import check_memory

from dtoolkit.transformer._util import transform_array_to_frame
from dtoolkit.transformer._util import transform_frame_to_series
from dtoolkit.transformer._util import transform_series_to_frame
from dtoolkit.transformer.base import Transformer


@doc(SKPipeline)
class Pipeline(SKPipeline):
    """
    Pipeline of transforms with a final estimator.

    Parameters
    ----------
    *args, **kwargs
        See the documentation for :class:`sklearn.pipeline.Pipeline` for complete
        details on the positional arguments and keyword arguments.

    See Also
    --------
    make_pipeline : DToolKit's version
    sklearn.pipeline.make_pipeline : sklearn's version

    Notes
    -----
    Different to :class:`sklearn.pipeline.Pipeline`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.
    """

    @doc(SKPipeline._fit)
    def _fit(self, X, y=None, **fit_params_steps):
        # shallow copy of steps - this should really be steps_
        self.steps = list(self.steps)
        self._validate_steps()

        # Setup the memory
        memory = check_memory(self.memory)
        fit_transform_one_cached = memory.cache(_fit_transform_one)

        for step_idx, name, transformer in self._iter(
            with_final=False,
            filter_passthrough=False,
        ):
            if transformer is None or transformer == "passthrough":
                with _print_elapsed_time("Pipeline", self._log_message(step_idx)):
                    continue

            if (
                hasattr(memory, "location")
                and memory.location is None
                or not hasattr(memory, "location")
                and hasattr(memory, "cachedir")
                and memory.cachedir is None
            ):
                # we do not clone when caching is disabled to
                # preserve backward compatibility
                cloned_transformer = transformer
            else:
                cloned_transformer = clone(transformer)

            # Fit or load from cache the current transformer
            Xt, fitted_transformer = fit_transform_one_cached(
                cloned_transformer,
                transform_series_to_frame(X),
                y,
                None,
                message_clsname="Pipeline",
                message=self._log_message(step_idx),
                **fit_params_steps[name],
            )
            X = transform_array_to_frame(Xt, X)

            # Replace the transformer of the step with the fitted
            # transformer. This is necessary when loading the transformer
            # from the cache.
            self.steps[step_idx] = (name, fitted_transformer)

        return transform_frame_to_series(X)

    @doc(SKPipeline._can_transform)
    def _can_transform(self):
        return super()._can_transform()

    @available_if(_can_transform)
    @doc(SKPipeline.transform)
    def transform(self, X):
        Xt = X
        for _, _, transformer in self._iter():
            Xt = transform_series_to_frame(Xt)
            Xt = transform_array_to_frame(transformer.transform(Xt), Xt)

        return transform_frame_to_series(Xt)

    @doc(SKPipeline.fit_transform)
    def fit_transform(self, X, y=None, **fit_params):
        fit_params_steps = self._check_fit_params(**fit_params)

        X = transform_series_to_frame(X)  # transform fit's input to DataFrame
        X = self._fit(X, y, **fit_params_steps)
        X = transform_series_to_frame(X)  # transofrm fit's output to DataFrame

        last_step = self._final_estimator
        with _print_elapsed_time("Pipeline", self._log_message(len(self.steps) - 1)):
            if last_step == "passthrough":
                return X

            fit_params_last_step = fit_params_steps[self.steps[-1][0]]
            if hasattr(last_step, "fit_transform"):
                Xt = last_step.fit_transform(X, y, **fit_params_last_step)
            else:
                Xt = last_step.fit(X, y, **fit_params_last_step).transform(X)

            Xt = transform_array_to_frame(Xt, X)
            return transform_frame_to_series(Xt)

    @doc(SKPipeline._can_inverse_transform)
    def _can_inverse_transform(self):
        return super()._can_inverse_transform()

    @available_if(_can_inverse_transform)
    @doc(SKPipeline.inverse_transform)
    def inverse_transform(self, Xt):
        reverse_iter = reversed(list(self._iter()))

        for _, _, transformer in reverse_iter:
            Xt = transform_series_to_frame(Xt)
            Xt = transform_array_to_frame(transformer.inverse_transform(Xt), Xt)

        return transform_frame_to_series(Xt)


def make_pipeline(
    *steps: list[Transformer],
    memory=None,
    verbose: bool = False,
) -> Pipeline:
    """
    Construct a :class:`Pipeline` from the given estimators.

    See Also
    --------
    Pipeline : DToolKit's version
    sklearn.pipeline.Pipeline : sklearn's version

    Notes
    -----
    Different to :func:`sklearn.pipeline.make_pipeline`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.
    """

    return Pipeline(_name_estimators(steps), memory=memory, verbose=verbose)


class FeatureUnion(SKFeatureUnion, Transformer):
    """
    Concatenates results of multiple transformer objects.

    See Also
    --------
    make_union : DToolKit's version
    sklearn.pipeline.make_union : sklearn's version

    Notes
    -----
    Different to :obj:`sklearn.pipeline.FeatureUnion`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.
    """

    def _hstack(self, Xs):
        if all(isinstance(i, (pd.Series, pd.DataFrame)) for i in Xs):
            # merge all into one DataFrame and the index would use the common part
            return pd.concat(Xs, axis=1, join="inner")

        return super()._hstack(Xs)


def make_union(
    *transformers: list[Transformer],
    n_jobs: int = None,
    verbose: bool = False,
) -> FeatureUnion:
    """
    Construct a FeatureUnion from the given transformers.

    See Also
    --------
    FeatureUnion : DToolKit's version
    sklearn.pipeline.FeatureUnion : sklearn's version

    Notes
    -----
    Different to :obj:`sklearn.pipeline.make_union`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.
    """

    return FeatureUnion(
        _name_estimators(transformers),
        n_jobs=n_jobs,
        verbose=verbose,
    )
