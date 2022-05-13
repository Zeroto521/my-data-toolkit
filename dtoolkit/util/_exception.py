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
        The level of stack.

    Examples
    --------
    >>> from warnings import warn
    >>> from dtoolkit.util._exception import find_stack_level
    >>> warn("Blah blah blah", stacklevel=find_stack_level())
    """

    pkg_dir = os.path.dirname(dtoolkit.__file__)
    test_dir = os.path.join(pkg_dir, "test")

    stack = inspect.stack()
    for n in range(len(stack)):
        fname = stack[n].filename

        if fname.startswith(pkg_dir) and not fname.startswith(test_dir):
            continue
        else:
            break

    return n
