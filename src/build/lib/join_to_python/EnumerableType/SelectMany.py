from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class SelectMany:
    """
    selectMany: Projects each element of a sequence to an IEnumerable<T>, and flattens the resulting sequences into one sequence using a selector function
    optionally, the transformation function can receive the index as a second argument
    an optional output transformation function processes the output of the selector function to produce an output

    >>> Enumerable<R> selectMany<T, TElement, R = TElement>(
        (Func<T, Iterable<TElement>> | Func<T, int, Iterable<TElement>) subSelectFunction,
        Func<T, TElement, R>? outputFunction = None);
    """
    def selectMany(self, subSelectFunction, outputFunction = None):
        if not subSelectFunction:
            raise ArgumentNullException("Required argument is None")

        # If not specified, then pass the element row out unchanged
        if not outputFunction:
            outputFunction = lambda src, row: row

        def _selectMany(data):
            index = 0
            for item in data:
                try:
                    checkArgumentCount(subSelectFunction, 2)
                    iter = subSelectFunction(item, index)
                except ArgumentCountException:
                    iter = subSelectFunction(item)
                index += 1

                for subItem in iter:
                    yield outputFunction(item, subItem)

        return self._extend(_selectMany)
