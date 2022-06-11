from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class Last:
    """
    last: Returns the last element in a sequence, throwing an exception if the sequence is empty.
    optional filter condition can be supplied
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    >>> T last<T>((Predicate<T> | Predicate<T, int>)? filterFunction = None);
    """
    def last(self, filterFunction = None):
        found = False
        index = 0
        for item in self:
            if not filterFunction:
                found = True
                lastItem = item
            else:
                try:
                    checkArgumentCount(filterFunction, 2)
                    if filterFunction(item, index):
                        found = True
                        lastItem = item
                except ArgumentCountException:
                    if filterFunction(item):
                        found = True
                        lastItem = item
            index += 1

        if (found):
            return lastItem

        raise EmptySequenceException("Sequence has no elements.")
