from __future__ import annotations

from functools import partial
from typing import Callable
from typing import Iterable
from typing import Literal


def parallelize(
    func: Callable,
    jobs: Iterable,
    *,
    n_jobs: int = -1,
    verbose: int = 0,
    timeout: float = None,
    backend: Literal["loky", "multiprocessing", "threading"] = "loky",
    require: Literal["sharedmem"] = None,
    mmap_mode: Literal[None, "r+", "r", "w+", "c"] = "r",
    **kwargs,
):
    """
    Parallelize ``func`` to do ``jobs``.

    A sugary syntax wraps :class:`joblib.Parallel`::

        from functools import partial

        from joblib import Parallel, delayed

        func = delayed(partial(func, **kwargs))
        Parallel(**parallel_kwargs)(map(func, jobs))

    Parameters
    ----------
    func : Callable

    jobs : Iterable

    n_jobs, verbose, timeout, backend, require, mmap_mode
        See the documentation for :class:`joblib.Parallel` for complete details on
        the keyword arguments.

    **kwargs
        See the documentation for ``func`` for complete details on the arguments.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'joblib'.

    See Also
    --------
    joblib.Parallel
    joblib.delayed

    Examples
    --------
    >>> from dtoolkit.util import parallelize
    >>> parallelize(lambda x: x ** 2, range(3))
    [0, 1, 4]
    """
    from joblib import Parallel, delayed

    func = delayed(partial(func, **kwargs))
    return Parallel(
        n_jobs=n_jobs,
        verbose=verbose,
        timeout=timeout,
        backend=backend,
        require=require,
        mmap_mode=mmap_mode,
    )(map(func, jobs))
