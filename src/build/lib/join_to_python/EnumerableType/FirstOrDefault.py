from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class FirstOrDefault:
    """
    firstOrDefault: Returns the first element in a sequence, throwing an exception if the sequence is empty.
    optional filter condition can be supplied
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    If the filtered sequence is empty, it returns the default value. The default value is provided by a parameter or is None.
    (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially not an empty sequence.)

    >>> T? firstOrDefault<T>((Predicate<T> | Predicate<T, int>)? filterFunction = None, T? defaultValue = None);
    """
    def firstOrDefault(self, filterFunction = None, defaultValue = None):
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

        return defaultValue
