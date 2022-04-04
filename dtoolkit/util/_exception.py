import inspect
import os.path

import dtoolkit


# based on pandas/util/_exceptions.py
def find_stack_level() -> int:
    """
    Find the first place in the stack that is not inside dtoolkit
    (tests notwithstanding).
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
