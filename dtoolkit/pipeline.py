from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.util._decorators import doc
from sklearn.base import clone
from sklearn.pipeline import _final_estimator_has
from sklearn.pipeline import _fit_transform_one
from sklearn.pipeline import _name_estimators
from sklearn.pipeline import FeatureUnion as SKFeatureUnion
from sklearn.pipeline import Pipeline as SKPipeline
from sklearn.utils import _print_elapsed_time
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import check_memory
from sklearn.utils.metadata_routing import _raise_for_params
from sklearn.utils.metadata_routing import process_routing

from dtoolkit._typing import OneDimArray
from dtoolkit._typing import SeriesOrFrame
from dtoolkit.transformer import Transformer
from dtoolkit.transformer._compat import SKLEARN_GE_14
from dtoolkit.transformer._util import transform_array_to_frame
from dtoolkit.transformer._util import transform_frame_to_series
from dtoolkit.transformer._util import transform_series_to_frame


__all__ = (
    "Pipeline",
    "FeatureUnion",
    "make_pipeline",
    "make_union",
)


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
    def _fit(self, X, y=None, routed_params=None) -> np.ndarray | SeriesOrFrame:
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

            if hasattr(memory, "location") and memory.location is None:
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
                params=routed_params[name],
            )
            X = transform_array_to_frame(Xt, X)

            # Replace the transformer of the step with the fitted
            # transformer. This is necessary when loading the transformer
            # from the cache.
            self.steps[step_idx] = (name, fitted_transformer)

        return transform_frame_to_series(X)

    def _can_transform(self):
        return super()._can_transform()

    @available_if(_can_transform)
    @doc(SKPipeline.transform)
    def transform(self, X, **params) -> np.ndarray | SeriesOrFrame:
        _raise_for_params(params, self, "transform")

        # not branching here since params is only available if
        # enable_metadata_routing=True
        routed_params = process_routing(self, "transform", **params)

        Xt = X
        for _, name, transformer in self._iter():
            Xt = transform_array_to_frame(
                transformer.transform(transform_series_to_frame(Xt)),
                **routed_params[name].transform,
            )

        return transform_frame_to_series(Xt)

    @doc(SKPipeline.fit_transform)
    def fit_transform(self, X, y=None, **params) -> np.ndarray | SeriesOrFrame:
        routed_params = self._check_method_params(method="fit_transform", props=params)

        X = self._fit(transform_series_to_frame(X), y, routed_params)
        X = transform_series_to_frame(X)  # transform fit's output to DataFrame

        last_step = self._final_estimator
        with _print_elapsed_time("Pipeline", self._log_message(len(self.steps) - 1)):
            if last_step == "passthrough":
                return X

            last_step_params = routed_params[self.steps[-1][0]]
            if hasattr(last_step, "fit_transform"):
                Xt = last_step.fit_transform(X, y, **last_step_params["fit_transform"])
            else:
                Xt = last_step.fit(Xt, y, **last_step_params["fit"]).transform(
                    X, **last_step_params["transform"]
                )

            return transform_frame_to_series(transform_array_to_frame(Xt, X))

    def _can_inverse_transform(self):
        return super()._can_inverse_transform()

    @available_if(_can_inverse_transform)
    @doc(SKPipeline.inverse_transform)
    def inverse_transform(self, Xt, **params) -> np.ndarray | SeriesOrFrame:
        _raise_for_params(params, self, "inverse_transform")

        # we don't have to branch here, since params is only non-empty if
        # enable_metadata_routing=True.
        routed_params = process_routing(self, "inverse_transform", **params)
        reverse_iter = reversed(list(self._iter()))

        for _, name, transformer in reverse_iter:
            Xt = transform_array_to_frame(
                transformer.inverse_transform(transform_series_to_frame(Xt)),
                **routed_params[name].inverse_transform,
            )

        return transform_frame_to_series(Xt)

    @available_if(_final_estimator_has("predict"))
    @doc(SKPipeline.predict)
    def predict(self, X, **params) -> OneDimArray:
        Xt = X

        if not _routing_enabled():
            for _, name, transform in self._iter(with_final=False):
                Xt = transform_series_to_frame(Xt)
                Xt = transform_array_to_frame(transformer.transform(Xt), Xt)

        else:
            # metadata routing enabled
            routed_params = process_routing(self, "predict", **params)
            for _, name, transform in self._iter(with_final=False):
                Xt = transform_series_to_frame(Xt)
                Xt = transform_array_to_frame(
                    transform.transform(Xt, **routed_params[name].transform), Xt
                )

            params = routed_params[self.steps[-1][0]].predict

        Xt = transform_series_to_frame(Xt)
        Xt = transform_array_to_frame(
            self.steps[-1][1].predict(Xt, **params),
            Xt,
        )
        return transform_frame_to_series(Xt, drop_name=True)

    @available_if(_final_estimator_has("fit_predict"))
    @doc(SKPipeline.predict)
    def fit_predict(self, X, y=None, **params) -> OneDimArray:
        routed_params = self._check_method_params(method="fit_predict", props=params)
        Xt = self._fit(X, y, routed_params)

        params_last_step = routed_params[self.steps[-1][0]]
        with _print_elapsed_time("Pipeline", self._log_message(len(self.steps) - 1)):
            y_pred = self.steps[-1][1].fit_predict(
                transform_series_to_frame(Xt),
                y,
                **fit_params_last_step,
            )
            y_pred = transform_array_to_frame(y_pred, y or Xt)

        return transform_frame_to_series(y_pred)


class FeatureUnion(SKFeatureUnion, Transformer):
    """
    Concatenates results of multiple transformer objects.

    See Also
    --------
    make_union
        Convenience function for simplified feature union construction.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.FeatureUnion`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

    Examples
    --------
    >>> from dtoolkit.pipeline import FeatureUnion
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> union = FeatureUnion([("pca", PCA(n_components=1)),
    ...                       ("svd", TruncatedSVD(n_components=2))])
    >>> X = [[0., 1., 3], [2., 2., 5]]
    >>> union.fit_transform(X)
    array([[ 1.5       ,  3.0...,  0.8...],
           [-1.5       ,  5.7..., -0.4...]])
    """

    def _hstack(self, Xs):
        if all(isinstance(i, (pd.Series, pd.DataFrame)) for i in Xs):
            # merge all into one DataFrame and the index would use the common part
            return pd.concat(Xs, axis=1, join="inner")

        return super()._hstack(Xs)


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
    >>> from dtoolkit.pipeline import make_pipeline
    >>> make_pipeline(StandardScaler(), GaussianNB(priors=None))
    Pipeline(steps=[('standardscaler', StandardScaler()),
                    ('gaussiannb', GaussianNB())])
    """

    return Pipeline(_name_estimators(steps), memory=memory, verbose=verbose)


def make_union(
    *transformers: list[Transformer],
    n_jobs: int = None,
    verbose: bool = False,
) -> FeatureUnion:
    """
    Construct a FeatureUnion from the given transformers.

    See Also
    --------
    FeatureUnion
        Class for concatenating the results of multiple transformer objects.

    Notes
    -----
    Different to :obj:`sklearn.pipeline.make_union`.
    This would let :obj:`~pandas.DataFrame` in and
    :obj:`~pandas.DataFrame` out.

    Examples
    --------
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> from dtoolkit.pipeline import make_union
    >>> make_union(PCA(), TruncatedSVD())
    FeatureUnion(transformer_list=[('pca', PCA()),
                                  ('truncatedsvd', TruncatedSVD())])
    """

    return FeatureUnion(
        _name_estimators(transformers),
        n_jobs=n_jobs,
        verbose=verbose,
    )
