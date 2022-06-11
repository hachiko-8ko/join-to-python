from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class InnerJoin:
    """
    innerJoin: A friendly helper to create a simple inner join. This combines the two key lookups and the custom equality comparer into a 
    single function input. For most programmers, this is all the complexity you'll need.
    This is JOIN-only (not in C#)

    >>> Enumerable<R> innerJoin<T, TSecond, R = ((T, TSecond))>(Iterable<TSecond> second, 
        Predicate<T, TSecond> on, Func<T, TSecond, R>? outputFunction = None);
    """
    def innerJoin(self, second, on, outputFunction = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not on:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _innerJoin(data):
            # Simple nested loops join
            # If this were SQL server, some analysis and pre-filtering could be done before comparison.
            # This isn't SQL Server. We can't even filter out NULLs, because what if the join function says "left == null && right == null", like some linq to entity queries do?

            # The right side can theoretically be a generator. We don't know, but we have to take that chance.
            # Python doesn't give a way to restart a generator, so we can only check right once without some extra BS to allow it to restart
            rightGen = RestartableGenerator(second)

            for leftItem in data:
                for rightItem in rightGen:
                    if on(leftItem, rightItem):
                        yield output(leftItem, rightItem)

                rightGen.restart()

        return self._extend(_innerJoin)
