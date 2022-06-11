#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *

"""
Basic Enumeration and Deferred Execution

JOIN to Python offers various operations such as filtering, projection, and counting on iterables such as lists. The JOIN slash methods can be called on any object, as in the example people/select(lambda q: q.firstName). This creates an Enumerable, which is the class behind every JOIN operation.

Ordinary map() and filter() functions called on lists execute when you call them. Methods in JOIN that return the Enumerable class only create the enumerable. They are not executed until you iterate them or call a method that produces a non-enumerable result. This is known as deferred execution.

Deferred execution in JOIN is managed through the use of Python generators, which produce records one by one while you iterate the generator, meaning that they both defer the start of the process and they halt when iteration is completed.

To show by way of example, the statements
    map(mapFunction, filter(filterFunction, arr))[0:5]
and
    arr/where(filterFunction)/select(mapFunction)/take(5)
produce the exact same results, but they have these differences:

    * the records in the list are processed that moment, while the records in the enumerable are not processed until you iterate them, such as using a for loop

    * filterFunction is called on every record of the list, while in the enumerable it is called only on enough records to produce 5 that match

    * mapFunction is called on every matching record of the list, while in the enumerable it is called at most 5 times

Methods that return a single result, such as count() or min() or first() or toArray() or toDictionary() will enumerate the list, the same as looping through with a for loop will.

Once you iterate an Enumerable, the query will be processed, and the generator providing the data is closed. In C# LINQ to Objects if you want to re-use query data, you call ToArray() on the query and capture the result, but JOIN to Python will cache the data returned so later iterations return from the cache. It's still good coding practice to be explicit and use toArray(), but you don't have to.
"""
class BasicTests(unittest.TestCase):
    def test(self):
        # Create a simple enumerable but do not trigger execution.
        queryable1 = [1, 2, 3]/select(lambda a: 3 * a)
        # This is a generator object
        print("> queryable1._source")
        print(queryable1._source)

        # I don't think there's any way to see the status of a generator without trying to iterate it.
        # I haven't been able to find the code, but the way Python normally works, it tells you it's done by throwing an exception, not
        # setting a visible property.
        # So we check the _isClosed flag set on generator close.
        test01 = queryable1._isClosed # should be false
        self.assertTrue(not test01, 'Queryable is not closed when created')

        # materialize the list
        queryable1/select(lambda p: p + 1)/toList()

        test02 = queryable1._isClosed # should be true
        self.assertTrue(test02, 'Queryable is closed when iterated')

        # Generators can only produce data once. If not for the cache, you'd have to specify the whole code
        # [1, 2, 3]/select(a => 3 * a) each time, or just store the list output.
        # But the Enumerable class caches the results when you pull them, so when the generator is closed, you pull from the cache.

        # This pulls from the cache. In a default generator, this would fail
        print("""\n> queryable1/toList()""")
        test03 = queryable1/toList()
        print(test03)
        self.assertEqual(len(test03), 3, 'toList still works after close')

        # takes a list, converts it to a queryable
        print("""\n> ['foo', 'bar', 'baz']/asQueryable()""")
        test04 = ['foo', 'bar', 'baz']/asQueryable()/toList()
        print(test04)
        self.assertTrue(test04[0] == 'foo' and test04[1] == 'bar' and test04[2] == 'baz', 'Enumerate an array')

        # calling asQueryable() on a string produces a character enumerable ... this has a,b,c
        print("""\n> 'abc'/asQueryable()""")
        test05 = 'abc'/asQueryable()/toList()
        print(test05)
        self.assertTrue(test05[0] == 'a' and test05[1] == 'b' and test05[2] == 'c', 'Strings can be converted to queryable')

        # calling asQueryable() on a number produces a range of numbers ... this is a 5-item enumerable having 0,1,2,3,4
        print("""\n> (5)/asQueryable()""")
        test06 = (5)/asQueryable()/toList()
        print(test06)
        self.assertTrue(len(test06) == 5 and test06/all_(lambda q, idx: q == idx), 'Numbers can be converted to queryable')

        # any iterable can be converted to a queryable
        print("""\n> randomGenerator()/asQueryable()""")
        # anything can be turned into a queryable, which enables the JOIN methods
        def randomGenerator():
            yield 1
            yield 4
            yield 16
        queryable2 = randomGenerator()/asQueryable()
        test07 = queryable2/toList()
        print(test07)
        self.assertTrue(test07[0] == 1 and test07[1] == 4 and test07[2] == 16, 'Iterables can be converted to a queryable')

        # though it's useless, non-iterable objects can be made queryable
        # this is a length 1 enumerable containing {name} as its only element
        print("""\n Object(name = 'Foo')/asQueryable()""")
        item = Object(name = 'Foo')
        test08 = item/asQueryable()/toList()
        print(test08)
        self.assertTrue(len(test08) == 1 and test08[0] == item, 'any object can be converted to a queryable')

        print("\nTEST 1: Test successful")

unittest.main()
