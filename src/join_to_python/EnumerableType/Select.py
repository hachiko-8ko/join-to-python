from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class Select:
    """
    select: projects each element of a sequence into a new form by calling a transformation function on each element.
    Optionally, the transformation function can receive the index as a second argument

    cast() is mapped to select() because in Python, cast() doesn't exist

    >>> Enumerable<TOut> select<T, TOut>(Func<T, TOut> | Func<T, int, TOut>) outputFunction);
    """
    def select(self, outputFunction):
        if not outputFunction:
            raise ArgumentNullException("Required argument is None")

        def _select(data):
            index = 0
            for item in data:
                try:
                    checkArgumentCount(outputFunction, 2)
                    yield outputFunction(item, index)
                except ArgumentCountException:
                    yield outputFunction(item)
                index += 1

        return self._extend(_select)
