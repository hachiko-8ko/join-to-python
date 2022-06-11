from .Base import *
from .Aggregate import *
from .All import *
from .Any import *
from .Append import *
from .Average import *
from .Chunk import *
from .Concat import *
from .Contains import *
from .Convert import *
from .Count import *
from .CrossJoin import *
from .DefaultIfEmpty import *
from .Distinct import *
from .DistinctBy import *
from .ElementAt import *
from .ElementAtOrDefault import *
from .Except import *
from .ExceptBy import *
from .First import *
from .FirstOrDefault import *
from .ForEach import *
from .FullJoin import *
from .GroupBy import *
from .GroupJoin import *
from .InnerJoin import *
from .Intersect import *
from .IntersectBy import *
from .Join import *
from .Last import *
from .LastOrDefault import *
from .LeftJoin import *
from .Max import *
from .MaxBy import *
from .MaxOrDefault import *
from .Min import *
from .MinBy import *
from .MinOrDefault import *
from .OfType import *
from .OuterJoin import *
from .Prepend import *
from .Replicate import *
from .Reverse import *
from .RightJoin import *
from .Select import *
from .SelectMany import *
from .SequenceEqual import *
from .Single import *
from .SingleOrDefault import *
from .Skip import *
from .SkipLast import *
from .SkipWhile import *
from .Step import *
from .Sum import *
from .Take import *
from .TakeLast import *
from .TakeWhile import *
from .Union import *
from .UnionBy import *
from .Where import *
from .Zip import *
from ..Types.Exceptions import *

class Enumerable(BaseEnumerable, Aggregate, All, Any, Append, Average, Chunk, Concat, Contains, Convert, Count, CrossJoin, DefaultIfEmpty, Distinct, DistinctBy, ElementAt, ElementAtOrDefault, Except, ExceptBy, First, FirstOrDefault, ForEach, FullJoin, GroupBy, GroupJoin, InnerJoin, Intersect, IntersectBy, Join, Last, LastOrDefault, LeftJoin, Max, MaxBy, MaxOrDefault, Min, MinBy, MinOrDefault, OfType, OuterJoin, Prepend, Replicate, Reverse, RightJoin, Select, SelectMany, SequenceEqual, Single, SingleOrDefault, Skip, SkipLast, SkipWhile, Step, Sum, Take, TakeLast, TakeWhile, Union, UnionBy, Where, Zip):
    def __init__(self, data):
        BaseEnumerable.__init__(self, data)

    # The circular reference prevent these from being split into different classes this can't be part of the base class.
    def _extend(self, func):
        """
        This helper allows methods declared in other files to use generator functions without referencing self._data() (requiring it
        to be public).
        """
        return Enumerable(func(self))

    @staticmethod
    def range(start, count):
        """
        range: return an enumerable containing count number of integers in a range, starting with start

        >>> static Enumerable<int> range(int start, int count);
        """
        if count < 0:
            raise OutOfRangeException("Argument out of range.")

        def _range():
            i = start
            maxval = start + count
            while i < maxval:
                yield i
                i += 1

        return Enumerable(_range())

    @staticmethod
    def repeat(element, count):
        """
        repeat: return an enumerable containing element count number of times

        >>> static Enumerable<T> repeat(T element, int count);
        """
        if count < 0:
            raise OutOfRangeException("Argument out of range.")

        def _repeat():
            i = 0
            while i < count:
                yield element
                i += 1

        return Enumerable(_repeat())

    """
    empty: Returns an empty IEnumerable<T> that doesn't have the specified type argument because this is Python

    >>> Enumerable<T> empty<T>();
    """
    def empty(self):
        return Enumerable([])
