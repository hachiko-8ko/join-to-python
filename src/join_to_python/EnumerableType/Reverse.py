from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

class Reverse:
    """
    reverse: Inverts the order of the elements in a sequence

    Reverse is really pointless. It is already found on the list class, and while this is technically
    delayed execution, it can only work by going through to the end of the enumerable.

    >>> Enumerable<T> reverse<T>();
    """
    def reverse(self):
        def _reverse(data):
            # While this is technically delayed execution, it obviously needs to process the entire dataset
            # because it has to get all the way to the last item before returning a row.
            yield from reversed(drain(data))

        return self._extend(_reverse)
