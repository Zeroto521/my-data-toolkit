from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


# based on more_itertools/more.py
def collapse(iterable: Iterable):
    def walk(node):
        if isinstance(node, (str, bytes)):
            yield node
            return

        try:
            tree = iter(node)
        except TypeError:
            yield node
            return
        else:
            for child in tree:
                yield from walk(child)

    yield from walk(iterable)
