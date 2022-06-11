import collections
from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

class Convert:
    def toArray(self):
        """
        toArray: Returns a Python list containing the sequence values

        >>> List<T> toArray<T>();
        """
        return self.toList()

    def toDictionary(self, keySelector, elementSelector = None):
        """
        toDictionary: Returns a dict with specified keys and values based on a keySelector function and an optional element selector function

        Note that in general, objects don't make good keys, but this will let you use them

        The C# ability to send a non-default equality comparer is not included because Python dicts do not allow custom equality.
        If you want, you can modify the __hash__ __eq__ method on the items themselves, but that is not controlled by the collection.

        >>> Dict<TKey, T | TElement> toDictionary<T, TKey, TElement>(Func<T, TKey> keySelector, Func<T, TElement>? elementSelector = None);
        """
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        result = collections.OrderedDict()
        for item in self:
            key = keySelector(item)
            if key in result:
                raise DuplicateException("Sequence contains duplicate keys")
            if elementSelector:
                result[key] = elementSelector(item)
            else:
                result[key] = item
        return result

    def toHashSet(self):
        """
        toHashSet: Returns a Set from an enumerable.
        The C# ability to send a non-default equality comparer is not included because Python sets do not allow custom equality.
        If you want, you can modify the __hash__ __eq__ method on the items themselves, but that is not controlled by the collection.

        >>> Set<T> toHashSet<T>();
        """
        result = set()
        for item in self:
            result.add(item)
        return result

    def toList(self):
        """
        toList: Returns a Python list containing the sequence values

        >>> List<T> toList<T>();
        """
        return drain(self)

    def toLookup(self, keySelector, elementSelector = None):
        """
        toLookup: Returns a defaultdict(list) with specified keys and values, based on a keySelector function and an optional element
        selector function. A defaultdict(list) is like a dict except it allows multiple values to be set for a given key.

        The C# ability to send a non-default equality comparer is not included because Python sets do not allow custom equality.
        If you want, you can modify the __hash__ __eq__ method on the items themselves, but that is not controlled by the collection.

        Note that in general, objects don't make good keys, but this will let you use them

        >>> DefaultDictList<TKey, T | TElement> toLookup<T, TKey, TElement>(Func<T, TKey> keySelector, Func<T, TElement>? elementSelector = None);
        """
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        result = collections.defaultdict(list)
        for item in self:
            key = keySelector(item)
            if elementSelector:
                result[key].append(elementSelector(item))
            else:
                result[key].append(item)
        return result
