from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class CrossJoin:
    """
    crossJoin: Create a simple cartesian join (every record from table 1 along with every record from table 2)
    This is JOIN-only (not in C#)

    >>> Enumerable<R> crossJoin<T, TSecond, R = ((T, TSecond))>(Iterable<TSecond> second, Func<T, TSecond, R>? outputFunction = None);
    """
    def crossJoin(self, second, outputFunction = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _crossJoin(data):
            # We need the ability to match the right side against every left side.
            # If it is a generator, it can't be restarted to allow that.
            rightGen = RestartableGenerator(second)
            for leftItem in data:
                for rightItem in rightGen:
                    yield output(leftItem, rightItem)
                rightGen.restart()

        return self._extend(_crossJoin)
