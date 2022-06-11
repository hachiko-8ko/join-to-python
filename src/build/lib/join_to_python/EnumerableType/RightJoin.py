from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class RightJoin:
    """
    rightJoin: A friendly helper to create a right left outer join. This follows the pattern of innerJoin(), which combines the two 
    key lookups and equality comparer into a single function input.
    This is JOIN-only (not in C#)

    >>> Enumerable<R> rightJoin<T, TSecond, R = ((T?, TSecond))>(Iterable<TSecond> second, Func<T, TSecond> on,
        Func<T, TSecond?, R>? outputFunction = None);
    """
    def rightJoin(self, second, on, outputFunction = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not on:
            raise ArgumentNullException("Required argument is None")

        if outputFunction:
            output = outputFunction
        else:
            # if function is missing, return tuple with (left, right)
            output = lambda l, r: (l, r)

        def _rightJoin(data):
            # Simple nested loops join
            # If this were SQL server, some analysis and pre-filtering could be done before comparison.
            # This isn't SQL Server. We can't even filter out NULLs, because what if the join function says "left == null && right == null", like some linq to entity queries do?

            # We need the ability to match the left side against every right side.
            # If it is a generator, it can't be restarted to allow that.
            leftGen = RestartableGenerator(data)
            for rightItem in second:
                rightMatched = False
                for leftItem in leftGen:
                    if on(leftItem, rightItem):
                        rightMatched = True
                        yield output(leftItem, rightItem)

                if not rightMatched:
                    yield output(None, rightItem)

                leftGen.restart()

        return self._extend(_rightJoin)
