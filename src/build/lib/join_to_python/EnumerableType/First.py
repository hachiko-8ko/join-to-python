from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class First:
    """
    first: Returns the first element in a sequence, throwing an exception if the sequence is empty.
    optional filter condition can be supplied
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    >>> T first<T>((Predicate<T> | Predicate<T, int>)? filterFunction = None);
    """
    def first(self, filterFunction = None):
        index = 0
        for item in self:
            if not filterFunction:
                return item
            else:
                try:
                    checkArgumentCount(filterFunction, 2)
                    if filterFunction(item, index):
                        return item
                except ArgumentCountException:
                    if filterFunction(item):
                        return item
            index += 1

        raise EmptySequenceException("Sequence has no elements.")
