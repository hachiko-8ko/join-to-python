from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class OuterJoin:
    """
    outerJoin_: Correlates the elements of two sequences based on matching keys. If no matching record is find in the second sequence, None is sent to the output selector.
    Outer Joins are not provided in LINQ. This is a new function, following the pattern of join()
    optional equality comparer can be used to compare keys
    If the output selector is left out, results are returned as (first row, second row).

    >>> Enumerable<R> outerJoin<T, TSecond, TKey, R = ((T, TSecond?))>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        Func<T, TSecond, R>? outputFunction = None, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def outerJoin(self, second, firstKeySelector, secondKeySelector, outputFunction = None, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not firstKeySelector or not secondKeySelector:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _outerJoin(data):
            # Simple nested loops join
            # If this were SQL server, some analysis and pre-filtering could be done before comparison.
            # This isn't SQL Server. We can't even filter out NULLs, because what if the join function says "left == null && right == null", like some linq to entity queries do?

            # The right side can theoretically be a generator. We don't know, but we have to take that chance.
            # If it is a generator, it can't be restarted to allow that.
            rightGen = RestartableGenerator(second)

            for leftItem in data:
                leftMatched = False
                leftKey = firstKeySelector(leftItem)
                for rightItem in rightGen:
                    rightKey = secondKeySelector(rightItem)
                    match = False
                    if comparer:
                        match = comparer(leftKey, rightKey)
                    else:
                        match = leftKey == rightKey
                    if match:
                        leftMatched = True
                        yield output(leftItem, rightItem)

                if not leftMatched:
                    yield output(leftItem, None)

                rightGen.restart()

        return self._extend(_outerJoin)
