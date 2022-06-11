from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class FullJoin:
    """
    fullJoin: A friendly helper to create a simple full outer join. This follows the pattern of innerJoin(), which combines the two
    key lookups and equality comparer into a single function input.
    This is JOIN-only (not in C#)

    >>> Enumerable<R> fullJoin<T, TSecond, R = ((T?, TSecond?))>(Iterable<TSecond> second, 
        Predicate<T, TSecond> on, Func<T?, TSecond?, R>? outputFunction = None);
    """
    def fullJoin(self, second, on, outputFunction = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not on:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _fullJoin(data):
            # Simple nested loops join
            # If this were SQL server, some analysis and pre-filtering could be done before comparison.
            # This isn't SQL Server. We can't even filter out NULLs, because what if the join function says "left == null && right == null", like some linq to entity queries do?

            # We need a place to track all items in the right that got sent
            sentRights = set()

            # We need the ability to match the right side against every left side.
            # If it is a generator, it can't be restarted to allow that.
            rightGen = RestartableGenerator(second)
            for leftItem in data:
                leftMatched = False
                for rightItem in rightGen:
                    if on(leftItem, rightItem):
                        leftMatched = True
                        sentRights.add(rightItem)
                        yield output(leftItem, rightItem)

                if not leftMatched:
                    yield output(leftItem, None)

                rightGen.restart()

            # Now go through the right side once more and send anything that didn't get sent
            for rightItem in rightGen:
                if rightItem not in sentRights:
                    yield output(None, rightItem)

        return self._extend(_fullJoin)
