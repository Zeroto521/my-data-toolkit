import inspect
import os.path

import dtoolkit


# based on pandas/util/_exceptions.py
def find_stack_level() -> int:
    """
    Find the first place in the stack that is not inside dtoolkit
    (test notwithstanding).

    Returns
    -------
    int
        The first place in the stack level.

    Examples
    --------
    >>> from warnings import warn
    >>> from dtoolkit.util._exception import find_stack_level
    >>> warn("Blah blah blah", stacklevel=find_stack_level())
    """

    pkg_dir = os.path.abspath(os.path.dirname(dtoolkit.__file__))
    test_dir = os.path.join(os.path.dirname(pkg_dir), "test")

    # https://stackoverflow.com/questions/17407119/python-inspect-stack-is-slow
    n = 0
    frame = inspect.currentframe()
    while frame:
        fname = inspect.getfile(frame)
        if not fname.startswith(pkg_dir) or fname.startswith(test_dir):
            break

        frame = frame.f_back
        n += 1

    return n
