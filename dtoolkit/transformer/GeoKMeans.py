from warnings import warn

import numpy as np
import scipy.sparse as sp
from pandas.util._decorators import doc
from sklearn.cluster import KMeans
from sklearn.cluster._k_means_common import _inertia_dense  # pylint: disable=E0611
from sklearn.cluster._k_means_common import _inertia_sparse  # pylint: disable=E0611
from sklearn.cluster._k_means_common import _is_same_clustering  # pylint: disable=E0611
from sklearn.cluster._k_means_elkan import elkan_iter_chunked_dense  # pylint: disable=E0611
from sklearn.cluster._k_means_elkan import elkan_iter_chunked_sparse  # pylint: disable=E0611
from sklearn.cluster._k_means_elkan import init_bounds_dense  # pylint: disable=E0611
from sklearn.cluster._k_means_elkan import init_bounds_sparse  # pylint: disable=E0611
from sklearn.cluster._kmeans import _kmeans_plusplus as sklearn_kmeans_plusplus
from sklearn.cluster._kmeans import _kmeans_single_elkan as sklearn_kmeans_single_elkan
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics.pairwise import haversine_distances
from sklearn.utils import check_array
from sklearn.utils import check_random_state
from sklearn.utils._openmp_helpers import _openmp_effective_n_threads  # pylint: disable=E0611
from sklearn.utils.extmath import stable_cumsum
from sklearn.utils.validation import _check_sample_weight
from sklearn.utils.validation import _is_arraylike_not_scalar
from sklearn.utils.validation import validate_data


class GeoKMeans(KMeans):
    """
    Spatial K-Means clustering.

    The distance is calculated by haversine formula.
    Parameters and attributes are the same as :class:`sklearn.cluster.KMeans`.

    Raises
    ------
    ValueError
        If the input is not in the form of ``[(longitude, latitude)]``.

    See Also
    --------
    sklearn.cluster.KMeans : Original implementation of K-Means clustering.

    Notes
    -----
    ``algorithm`` is fixed to ``"elkan"``. Because only elkan algorithm can support
    custom distance.

    Examples
    --------
    >>> from dtoolkit.transformer import GeoKMeans
    >>> X = [
    ...     [113.615822, 37.844797],
    ...     [113.586288, 37.917018],
    ...     [113.630711, 37.865369],
    ...     [113.590684, 37.948056],
    ...     [113.631483, 37.862634],
    ...     [113.57413, 37.968669],
    ...     [113.663159, 37.848446],
    ...     [113.586941, 37.868116],
    ...     [113.679381, 37.875028],
    ...     [113.5706, 37.973542],
    ...     [113.585504, 37.879261],
    ...     [113.584412, 37.935521],
    ...     [113.575964, 37.906472],
    ...     [113.593658, 37.848911],
    ...     [113.633605, 37.869107],
    ...     [113.582298, 37.857025],
    ...     [113.629378, 37.805196],
    ...     [113.48768, 37.872603],
    ...     [113.477766, 37.868846],
    ... ]
    >>> geokmeans = GeoKMeans(n_clusters=2, random_state=0).fit(X)
    >>> geokmeans.labels_
    array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
          dtype=int32)
    >>> geokmeans.cluster_centers_
    array([[113.5559405 ,  37.92384087],
           [113.62108545,  37.85671727]])
    """

    def __init__(
        self,
        n_clusters=8,
        *,
        init="k-means++",
        n_init="auto",
        max_iter=300,
        tol=1e-4,
        verbose=0,
        random_state=None,
        copy_x=True,
        algorithm="elkan",
    ):
        super().__init__(
            n_clusters=n_clusters,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            # NOTE: algorithm is always "elkan", because only "elkan" supports
            # haversine distance.
            algorithm="elkan",  # !!!: GeoKMeans different from KMeans
        )

    def _validate_coordinate(self, X):  # !!!: GeoKMeans different from KMeans
        if not (
            X.ndim == 2
            and X.shape[1] == 2
            and all(X[:, 0] >= -180)
            and all(X[:, 0] <= 180)
            and all(X[:, 1] >= -90)
            and all(X[:, 1] <= 90)
        ):
            raise ValueError("'X' must be in the form of [(longitude, latitude)]")

    # based on github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_kmeans.py
    @doc(KMeans._init_centroids)
    def _init_centroids(
        self,
        X,
        x_radians,
        init,
        random_state,
        sample_weight,
        init_size=None,
        n_centroids=None,
    ):
        n_samples = X.shape[0]
        n_clusters = self.n_clusters if n_centroids is None else n_centroids

        if init_size is not None and init_size < n_samples:
            init_indices = random_state.randint(0, n_samples, init_size)
            X = X[init_indices]
            x_radians = x_radians[init_indices]
            n_samples = X.shape[0]
            sample_weight = sample_weight[init_indices]

        if isinstance(init, str) and init == "k-means++":
            centers, _ = _kmeans_plusplus(  # !!!: GeoKMeans different from KMeans
                X,
                n_clusters,
                random_state=random_state,
                x_radians=x_radians,
                sample_weight=sample_weight,
            )
        elif isinstance(init, str) and init == "random":
            seeds = random_state.choice(
                n_samples,
                size=n_clusters,
                replace=False,
                p=sample_weight / sample_weight.sum(),
            )
            centers = X[seeds]
        elif _is_arraylike_not_scalar(self.init):
            centers = init
        elif callable(init):
            centers = init(X, n_clusters, random_state=random_state)
            centers = check_array(centers, dtype=X.dtype, copy=False, order="C")
            self._validate_center_shape(X, centers)

        return centers.toarray() if sp.issparse(centers) else centers

    # based on github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_kmeans.py
    @doc(KMeans.fit)
    def fit(self, X, y=None, sample_weight=None):
        X = validate_data(
            self,
            X,
            accept_sparse="csr",
            dtype=[np.float64, np.float32],
            order="C",
            copy=self.copy_x,
            accept_large_sparse=False,
        )

        self._validate_coordinate(X)  # !!!: GeoKMeans different from KMeans
        self._check_params_vs_input(X)

        random_state = check_random_state(self.random_state)
        sample_weight = _check_sample_weight(sample_weight, X, dtype=X.dtype)
        self._n_threads = _openmp_effective_n_threads()

        # Validate init array
        init = self.init
        init_is_array_like = _is_arraylike_not_scalar(init)
        if init_is_array_like:
            init = check_array(init, dtype=X.dtype, copy=True, order="C")
            self._validate_center_shape(X, init)
        # subtract of mean of x for more accurate distance computations
        if not sp.issparse(X):
            X_mean = X.mean(axis=0)
            # The copy was already done above
            X -= X_mean

            if init_is_array_like:
                init -= X_mean

        # precompute radian of data points
        x_radians = np.radians(X)  # !!!: GeoKMeans different from KMeans

        best_inertia, best_labels = None, None

        for _ in range(self._n_init):
            # Initialize centers
            centers_init = self._init_centroids(  # !!!: GeoKMeans different from KMeans
                X,
                x_radians,
                init,
                random_state,
                sample_weight,
            )
            if self.verbose:
                print("Initialization complete")

            # run a k-means once
            labels, inertia, centers, n_iter_ = _kmeans_single_elkan(
                X,
                sample_weight,
                centers_init,
                max_iter=self.max_iter,
                verbose=self.verbose,
                tol=self._tol,
                n_threads=self._n_threads,
            )

            # determine if these results are the best so far
            # we chose a new run if it has a better inertia and the clustering is
            # different from the best so far (it's possible that the inertia is
            # slightly better even if the clustering is the same with potentially
            # permuted labels, due to rounding errors)
            if best_inertia is None or (
                inertia < best_inertia
                and not _is_same_clustering(labels, best_labels, self.n_clusters)
            ):
                best_labels = labels
                best_centers = centers
                best_inertia = inertia
                best_n_iter = n_iter_

        if not sp.issparse(X):
            if not self.copy_x:
                X += X_mean
            best_centers += X_mean

        if (distinct_clusters := len(set(best_labels))) < self.n_clusters:
            warn(
                f"Number of distinct clusters ({distinct_clusters}) found smaller than "
                f"n_clusters ({self.n_clusters}). Possibly due to duplicate points in "
                "X.",
                ConvergenceWarning,
                stacklevel=2,
            )

        self.cluster_centers_ = best_centers
        self._n_features_out = self.cluster_centers_.shape[0]
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        self.n_iter_ = best_n_iter

        return self

    def _transform(self, X):
        """Guts of transform method; no input validation."""

        self._validate_coordinate(X)
        # !!!: GeoKMeans different from KMeans
        return haversine_distances(np.radians(X), np.radians(self.cluster_centers_))


# based on github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_kmeans.py
@doc(sklearn_kmeans_single_elkan)
def _kmeans_single_elkan(
    X,
    sample_weight,
    centers_init,
    max_iter=300,
    verbose=False,
    tol=1e-4,
    n_threads=1,
):
    n_samples = X.shape[0]
    n_clusters = centers_init.shape[0]

    # Buffers to avoid new allocations at each iteration.
    centers = centers_init
    centers_new = np.zeros_like(centers)
    weight_in_clusters = np.zeros(n_clusters, dtype=X.dtype)
    labels = np.full(n_samples, -1, dtype=np.int32)
    labels_old = labels.copy()
    # !!!: GeoKMeans different from KMeans
    center_half_distances = haversine_distances(np.radians(centers)) / 2
    distance_next_center = np.partition(
        np.asarray(center_half_distances),
        kth=1,
        axis=0,
    )[1]
    upper_bounds = np.zeros(n_samples, dtype=X.dtype)
    lower_bounds = np.zeros((n_samples, n_clusters), dtype=X.dtype)
    center_shift = np.zeros(n_clusters, dtype=X.dtype)

    if sp.issparse(X):
        init_bounds = init_bounds_sparse
        elkan_iter = elkan_iter_chunked_sparse
        _inertia = _inertia_sparse
    else:
        init_bounds = init_bounds_dense
        elkan_iter = elkan_iter_chunked_dense
        _inertia = _inertia_dense

    init_bounds(
        X,
        centers,
        center_half_distances,
        labels,
        upper_bounds,
        lower_bounds,
        n_threads=n_threads,
    )

    strict_convergence = False

    for i in range(max_iter):
        elkan_iter(
            X,
            sample_weight,
            centers,
            centers_new,
            weight_in_clusters,
            center_half_distances,
            distance_next_center,
            upper_bounds,
            lower_bounds,
            labels,
            center_shift,
            n_threads,
        )

        # compute new pairwise distances between centers and closest other
        # center of each center for next iterations
        # !!!: GeoKMeans different from KMeans
        distance_next_center = np.partition(
            np.asarray(haversine_distances(np.radians(centers_new)) / 2),
            kth=1,
            axis=0,
        )[1]

        if verbose:
            inertia = _inertia(X, sample_weight, centers, labels, n_threads)
            print(f"Iteration {i}, inertia {inertia}")

        centers, centers_new = centers_new, centers

        if np.array_equal(labels, labels_old):
            # First check the labels for strict convergence.
            if verbose:
                print(f"Converged at iteration {i}: strict convergence.")
            strict_convergence = True
            break
        else:
            # No strict convergence, check for tol based convergence.
            center_shift_tot = (center_shift**2).sum()
            if center_shift_tot <= tol:
                if verbose:
                    print(
                        f"Converged at iteration {i}: center shift "
                        f"{center_shift_tot} within tolerance {tol}.",
                    )
                break

        labels_old[:] = labels

    if not strict_convergence:
        # rerun E-step so that predicted labels match cluster centers
        elkan_iter(
            X,
            sample_weight,
            centers,
            centers,
            weight_in_clusters,
            center_half_distances,
            distance_next_center,
            upper_bounds,
            lower_bounds,
            labels,
            center_shift,
            n_threads,
            update_centers=False,
        )

    inertia = _inertia(X, sample_weight, centers, labels, n_threads)
    return labels, inertia, centers, i + 1


# based on github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_kmeans.py
@doc(sklearn_kmeans_plusplus)
def _kmeans_plusplus(
    X,
    n_clusters,
    x_radians,
    sample_weight,
    random_state,
    n_local_trials=None,
):
    n_samples, n_features = X.shape
    centers = np.empty((n_clusters, n_features), dtype=X.dtype)

    # Set the number of local seeding trials if none is given
    if n_local_trials is None:
        # This is what Arthur/Vassilvitskii tried, but did not report
        # specific results for other than mentioning in the conclusion
        # that it helped.
        n_local_trials = 2 + int(np.log(n_clusters))

    # Pick first center randomly and track index of point
    center_id = random_state.choice(n_samples, p=sample_weight / sample_weight.sum())
    indices = np.full(n_clusters, -1, dtype=int)
    if sp.issparse(X):
        centers[0] = X[[center_id]].toarray()
    else:
        centers[0] = X[center_id]
    indices[0] = center_id

    # Initialize list of closest distances and calculate current potential
    # !!!: GeoKMeans different from KMeans
    closest_dist_sq = haversine_distances(np.radians(centers[0, np.newaxis]), x_radians)
    current_pot = closest_dist_sq @ sample_weight

    # Pick the remaining n_clusters-1 points
    for c in range(1, n_clusters):
        # Choose center candidates by sampling with probability proportional
        # to the squared distance to the closest existing center
        rand_vals = random_state.uniform(size=n_local_trials) * current_pot
        candidate_ids = np.searchsorted(
            stable_cumsum(sample_weight * closest_dist_sq),
            rand_vals,
        )
        # XXX: numerical imprecision can result in a candidate_id out of range
        np.clip(candidate_ids, None, closest_dist_sq.size - 1, out=candidate_ids)

        # Compute distances to center candidates
        # !!!: GeoKMeans different from KMeans
        distance_to_candidates = haversine_distances(
            x_radians[candidate_ids],
            x_radians,
        )

        # update closest distances squared and potential for each candidate
        np.minimum(closest_dist_sq, distance_to_candidates, out=distance_to_candidates)
        candidates_pot = distance_to_candidates @ sample_weight.reshape(-1, 1)

        # Decide which candidate is the best
        best_candidate = np.argmin(candidates_pot)
        current_pot = candidates_pot[best_candidate]
        closest_dist_sq = distance_to_candidates[best_candidate]
        best_candidate = candidate_ids[best_candidate]

        # Permanently add best center candidate found in local tries
        if sp.issparse(X):
            centers[c] = X[[best_candidate]].toarray()
        else:
            centers[c] = X[best_candidate]
        indices[c] = best_candidate

    return centers, indices
