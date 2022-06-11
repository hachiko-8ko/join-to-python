from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class Join:
    """
    join: Correlates the elements of two sequences based on matching keys. Only records are returned when both sides match.
    optional equality comparer can be used to compare keys.

    If the output selector is left out, results are returned as (first row, second row). This is a change from C#, which requires the output selector.

    >>> Enumerable<R> join<T, TSecond, TKey, R = ((T, TSecond))>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        Func<T, TSecond, R>? outputFunction = None, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def join(self, second, firstKeySelector, secondKeySelector, outputFunction = None, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not firstKeySelector or not secondKeySelector:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _join(data):
            # Simple nested loops join
            # If this were SQL server, some analysis and pre-filtering could be done before comparison.
            # This isn't SQL Server. We can't even filter out NULLs, because what if the join function says "left == null && right == null", like some linq to entity queries do?

            # The right side can theoretically be a generator. We don't know, but we have to take that chance.
            # If it is a generator, it can't be restarted to allow that.
            rightGen = RestartableGenerator(second)

            for leftItem in data:
                leftKey = firstKeySelector(leftItem)
                for rightItem in rightGen:
                    rightKey = secondKeySelector(rightItem)
                    match = False
                    if comparer:
                        match = comparer(leftKey, rightKey)
                    else:
                        match = leftKey == rightKey
                    if match:
                        yield output(leftItem, rightItem)

                rightGen.restart()

        return self._extend(_join)
