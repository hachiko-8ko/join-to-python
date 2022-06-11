from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class Single:
    """
    single: Returns the last element in a sequence, throwing an exception if the sequence is empty.
    optional filter condition can be supplied
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    >>> T single<T>((Predicate<T> | Predicate<T, int>)? filterFunction = None);
    """
    def single(self, filterFunction = None):
        found = False
        index = 0
        for item in self:
            if not filterFunction:
                if (found):
                    raise DuplicateException("Sequence contains more than one element")
                found = True
                foundItem = item
            else:
                try:
                    checkArgumentCount(filterFunction, 2)
                    if filterFunction(item, index):
                        if (found):
                            raise DuplicateException("Sequence contains more than one element")
                        found = True
                        foundItem = item
                except ArgumentCountException:
                    if filterFunction(item):
                        if (found):
                            raise DuplicateException("Sequence contains more than one element")
                        found = True
                        foundItem = item
            index += 1

        if found:
            return foundItem

        raise EmptySequenceException("Sequence has no elements.")
