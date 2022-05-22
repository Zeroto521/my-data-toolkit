from pandas.util._decorators import doc
from sklearn.base import clone
from sklearn.pipeline import _fit_transform_one
from sklearn.pipeline import Pipeline as SKPipeline
from sklearn.utils import _print_elapsed_time
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import check_memory

from dtoolkit.transformer._util import transform_array_to_frame
from dtoolkit.transformer._util import transform_frame_to_series
from dtoolkit.transformer._util import transform_series_to_frame


class Pipeline(SKPipeline):
    # TODO: Overwrite `predict` and `fit_predict` method
    # let Pandas-Object in Pandas-Object out

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
