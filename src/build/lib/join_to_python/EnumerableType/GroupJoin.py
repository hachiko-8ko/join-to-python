from ..Generators.RestartableGenerator import *
from..Types.EqualityComparer import *
from ..Types.Grouping import *
from ..Types.Exceptions import *

class GroupJoin:
    """
    groupJoin: Correlates the elements of two sequences based on key equality and groups the results.

    This is a sort of a combination of outer join and half a group by (only the second sequence is grouped).
    The output function, which determines the output, is required. This doesn't seem useful enough for me to come up with a default output.

    >>> Enumerable<TResult> groupJoin<T, TSecond, TKey, TResult>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        Func<T, TSecond[], TResult> outputFunction, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def groupJoin(self, second, firstKeySelector, secondKeySelector, outputFunction, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not firstKeySelector or not secondKeySelector or not outputFunction:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _groupJoin(data):
            # We need the ability to check the right side against every left side.
            # If it is a generator, it can't be restarted to allow that.
            rightGen = RestartableGenerator(second)
            right = []
            for leftItem in data:
                grouping = None
                for rightItem in rightGen:
                    match = False
                    leftKey = firstKeySelector(leftItem)
                    rightKey = secondKeySelector(rightItem)

                    if compare:
                        match = compare(leftKey, rightKey)
                    else:
                        match = leftKey == rightKey

                    if match:
                        if grouping:
                            grouping.add(rightItem)
                        else:
                            grouping = Grouping(leftKey, rightItem)

                if grouping:
                    yield outputFunction(leftItem, grouping.values)
                else:
                    yield outputFunction(leftItem, [])

                rightGen.restart()

        return self._extend(_groupJoin)
