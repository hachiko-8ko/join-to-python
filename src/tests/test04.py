#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *

"""
Advanced Single-Sequence Queries

This test deals with more advanced queries that can be called on a single iterable.
"""
class AdvancedSingleSequenceTests(unittest.TestCase):
    def test(self):
        # should be [1,2,3] (not empty so it passes through)
        print("""> [1, 2, 3]/defaultIfEmpty()/toList()""")
        test01 = [1, 2, 3]/defaultIfEmpty()/toList()
        print(test01)
        self.assertListEqual(test01, [1, 2, 3], 'DefaultIfEmpty when not empty')

        # [-1] when no data
        print("""\n> []/defaultIfEmpty(-1)/toList()""")
        test02 = []/defaultIfEmpty(-1)/toList()
        print(test02)
        self.assertTrue(len(test02) == 1 and test02[0] == -1, 'DefaultIfEmpty supplies row when empty iterable')

        # 1,2,3,4
        print("""\n> [1, 2, 3]/append(4)/toList()""")
        test03 = [1, 2, 3]/append(4)/toList()
        print(test03)
        self.assertListEqual(test03, [1, 2, 3, 4], 'Append adds to end of sequence')

        # should be "new first","first","second" (adds new first to start)
        print("""\n> ['first', 'second']/prepend('new first')/toList()""")
        test04 = ['first', 'second']/prepend('new first')/toList()
        print(test04)
        self.assertListEqual(test04, ['new first', 'first', 'second'], 'Prepend adds to beginning of sequence')

        # reverse the list
        print("""\n> [2, 4, 6, 1, 3, 5, 7]/reverse()/toList()""")
        test05 = [2, 4, 6, 1, 3, 5, 7]/reverse()/toList()
        print(test05)
        self.assertListEqual(test05, [7, 5, 3, 1, 6, 4, 2], 'Reverse reverses all elements')

        # concatenates the sequence with itself n times
        # this is another JOIN-specific method not in LINQ
        print("""\n> ["A", "B", "C"]/replicate(3)/toList()""")
        test06 = ["A", "B", "C"]/replicate(3)/toList()
        print(test06)
        self.assertListEqual(test06, ["A", "B", "C", "A", "B", "C", "A", "B", "C"], 'Replicate repeats an array')

        # create an empty array of the same type as sequence ... ok, except that type means nothing in Python so this is REALLY useless
        print("""\n> ['a', 'b', 1, 2]/empty()/toList()""")
        test07 = ['a', 'b', 1, 2]/empty()/toList()
        print(test07)
        self.assertEqual(len(test07), 0, 'Empty() returns empty enumerable')

        # break array into chunks of provided size
        print("""\n> [1, 2, 3, 4, 5, 6, 7, 8]/chunk(3)/toList()""")
        test08 = [1, 2, 3, 4, 5, 6, 7, 8]/chunk(3)/toList()
        print(test08)
        self.assertEqual(str(test08), "[[1, 2, 3], [4, 5, 6], [7, 8]]", "Chunk breaks iterable into chunks")

        # verify even chunk size case
        print("""\n> [1, 2, 3, 4, 5, 6, 7, 8, 9]/chunk(3)/toList()""")
        test08a = [1, 2, 3, 4, 5, 6, 7, 8, 9]/chunk(3)/toList()
        print(test08a)
        self.assertEqual(str(test08a), "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]", "Chunk breaks iterable into equal size chunks")

        # orderBy() and orderByDescending() order by the result of a provided key selector method.
        # The result of the two orderBy methods are enumerables that have two methods not found in default Enumerables:
        #       OrderedEnumerable<T> thenBy<TKey>(Func<T, TKey>? orderBy = None, IComparer<TKey>? comparer = None);
        #       OrderedEnumerable<T> thenByDescending<TKey>(Func<T, TKey>? orderBy = None, IComparer<TKey>? comparer = None);

        # The best part is that in addition to being a cleaner API, they actually work. If you've ever tried to use sorted()
        # or list.sort() to sort multiple keys, and watched them fail to act as documented, you'd welcome this.

        # order by word length then reverse alphabetical
        print("""\n> ['dog', 'fish', 'cat', 'bird', 'iguana', 'turtle']/orderBy(lambda o: len(o))/thenByDescending()/toList()""")
        test09 = ['dog', 'fish', 'cat', 'bird', 'iguana', 'turtle']/orderBy(lambda o: len(o))/thenByDescending(lambda abc: abc)/toList()
        print(test09)
        self.assertListEqual(test09, ["dog", "cat", "fish", "bird", "turtle", "iguana"], 'OrderBy() followed by ThenByDescending()')

        # reverse length then alphabetical ... empty keySelector is the same as lambda key: key
        print("""\n> ['dog', 'fish', 'cat', 'bird', 'iguana', 'turtle']/orderByDescending(lambda o: len(o))/thenBy()/toList()""")
        test10 = ['dog', 'fish', 'cat', 'bird', 'iguana', 'turtle']/orderByDescending(lambda o: len(o))/thenBy()/toList()
        print(test10)
        self.assertListEqual(test10, ["iguana", "turtle", "bird", "fish", "cat", "dog"], 'OrderByDescending() followed by ThenBy()')

        # The folks at Microsoft gave us a lot of overloads for GroupBy(), most of them not really necessary or extremely useful.
        # So here goes a bunch of testing of the same method.

        # Group by first letter
        print("""\n> fruits = ['Apple', 'Canteloupe', 'Banana', 'Apricot', 'Blueberry']""")
        fruits = ['Apple', 'Canteloupe', 'Banana', 'Apricot', 'Blueberry']
        print("""> fruits/groupBy(lambda q: q[0])/toList()""")
        test11 = fruits/groupBy(lambda q: q[0])/toList()
        print(test11)

        # This is annoying to test with nested lists
        def getGroupLen(arr, key):
            grp = arr/where(lambda w: w.key == key)/toList()/first()
            return len([x for x in grp.values if x[0] == key])
        self.assertTrue((len(test11) == 3 and
            getGroupLen(test11, 'A') == 2 and
            getGroupLen(test11, 'B') == 2 and
            getGroupLen(test11, 'C') == 1
            ), 'Basic GroupBy')

        # While the result of the group operation is an iterable that appears as if it's just an array, it's actually an object that contains fields named 'key' and 'values'

        # see the keys of each group
        print("""\n> [x.key for x in fruits/groupBy(lambda q: q[0])/toList()]""")
        test12 = [x.key for x in fruits/groupBy(lambda q: q[0])/toList()]
        print(test12)
        self.assertListEqual(test12, ["A", "C", "B"], "Access key of grouping")

        # can take an optional transformation to be applied to grouping elements
        print("""\n> fruits/groupBy(lambda q: q[0], lambda u: u.upper())/toList()""")
        test13 = fruits/groupBy(lambda q: q[0], lambda u: u.upper())/toList()
        print(test13)
        # These are basically the same test and the output is consistent
        self.assertEqual(str(test11).upper(), str(test13), "GroupBy with element function")

        # can take an optional output transformation to be projected onto the returned groupings
        print("""\n> fruits/groupBy(lambda q: q[0], lambda u: u.upper(), lambda k, d: "{k} is for {j}".format(k=k,j=' and '.join(d)))/toList()""")
        test14 = fruits/groupBy(lambda q: q[0], lambda u: u.upper(), lambda k, d: "{k} is for {j}".format(k=k,j=' and '.join(d)))/toList()
        print(test14)
        self.assertListEqual(test14, ["A is for APPLE and APRICOT", "C is for CANTELOUPE", "B is for BANANA and BLUEBERRY"], "GroupBy with output function")

        # can take a custom equality comparer, such as one that makes matching case equal
        print("""\n> [Too complicated to print. Look at the code.]""")
        test15 = (['Apple', 'canteloupe', 'Banana', 'Apricot', 'blueberry']/groupBy(lambda q: q[0], lambda u: u + '!', 
                lambda k, d: "{j} start with {u}".format(j=' and '.join(d),u='capital' if k.upper() == k else 'lowercase'), 
                lambda a, b: (a.upper() == a) == (b.upper() == b))
            /toList())
        print(test15)
        self.assertListEqual(test15, ["Apple! and Banana! and Apricot! start with capital", "canteloupe! and blueberry! start with lowercase"], "GroupBy with custom equality")

        # custom equality but no element or output functions
        print("""\n> ['Apple', 'canteloupe', 'Banana', 'Apricot', 'blueberry']/groupBy(lambda q: q[0], comparer = lambda a, b: (a.upper() == a) == (b.upper() == b))/toList()""")
        test16 = ['Apple', 'canteloupe', 'Banana', 'Apricot', 'blueberry']/groupBy(lambda q: q[0], comparer = lambda a, b: (a.upper() == a) == (b.upper() == b))/toList()
        print(test16)
        # going to try and shortcut with a string here
        self.assertEqual(str(test16), """[['Apple', 'Banana', 'Apricot'], ['canteloupe', 'blueberry']]""", 'GroupBy with only equality')

        # custom output projector only
        print("""\n> fruits/groupBy(lambda q: q[0], outputFunction = lambda k, d: "{k} is for {j}".format(k=k,j=' and '.join(d)))/toList()""")
        test17 = fruits/groupBy(lambda q: q[0], outputFunction = lambda k, d: "{k} is for {j}".format(k=k,j=' and '.join(d)))/toList()
        print(test17)
        self.assertListEqual(test17, ["A is for Apple and Apricot", "C is for Canteloupe", "B is for Banana and Blueberry"], "GroupBy with only projector")

        # everything but element function
        print("""\n> [Too complicated to print. Look at the code.]""")
        test18 = (['Apple', 'canteloupe', 'Banana', 'Apricot', 'blueberry']/groupBy(lambda q: q[0], 
                outputFunction = lambda k, d: "{j} start with {u}".format(j=' and '.join(d),u='capital' if k.upper() == k else 'lowercase'),
                comparer = lambda a, b: (a.upper() == a) == (b.upper() == b))
            /toList())
        print(test18)
        self.assertListEqual(test18, ["Apple and Banana and Apricot start with capital", "canteloupe and blueberry start with lowercase"], "GroupBy with no element function")

        # everything but output projector
        print("""\n> [Too complicated to print. Look at the code.]""")
        test19 = (['Apple', 'canteloupe', 'Banana', 'Apricot', 'blueberry']/groupBy(lambda q: q[0], 
                elementFunction = lambda q: q + '!',
                comparer = lambda a, b: (a.upper() == a) == (b.upper() == b))
            /toList())
        print(test19)
        # another lazy test here
        self.assertEqual(str(test19), """[['Apple!', 'Banana!', 'Apricot!'], ['canteloupe!', 'blueberry!']]""", 'GroupBy with no output function')

        # Test static methods on Enumerable (not part of IQueryable, but still in System.Linq)...
        # System.Linq also includes two static non-extension methods. This one is almost the same as range()
        print("""\n> Enumerable.range(2, 10)/toList()""")
        test20 = Enumerable.range(2, 10)/toList()
        print(test20)
        self.assertListEqual(test20, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'Range() returns a range of numbers')

        # this is the other. It's basically the same as ['spam'] * 4 but with deferred execution
        print("""\n> Enumerable.repeat("spam", 4)/toList()""")
        test21 = Enumerable.repeat("spam", 4)/toList()
        print(test21)
        self.assertListEqual(test21, ["spam", "spam", "spam", "spam"], 'Repeat() repeats an element')

        # Normally to count an enumerable, you must enumerate it, materializing its data.
        # LINQ provides this method, tryGetNonEnumeratedCount(), which tries to get the count from the underlying object, when possible
        # It works using an out var, like all TryGetSomething() methods in C#. This doesn't exist in Python. 
        # To make it work, you need to pass an dictionary, which is updated.

        # The way you normally would use it would be:
        # if enum/tryGetNonEnumeratedCount(countVal):
        #    doSomethingWith(countVal["value"])

        # now "value" can be updated and the reference returned
        print("""\n> countVal = { "value": 0 }""")
        countVal = { "value": 0 }

        print("""> [1, 2, 3, 4]/tryGetNonEnumeratedCount(countVal)""")
        count1 = [1, 2, 3, 4]/tryGetNonEnumeratedCount(countVal)
        print(count1, countVal['value'])
        self.assertTrue(count1 and countVal['value'] == 4, "tryGetNonEnumeratedCount returned array count")

        countVal['value'] = 0

        # you can also count strings without enumeration
        print("""> 'nothing is something worth doing'/tryGetNonEnumeratedCount(countVal)""")
        count1a = 'nothing is something worth doing'/tryGetNonEnumeratedCount(countVal)
        print(count1a, countVal['value'])
        self.assertTrue(count1a and countVal['value'] == 32, "tryGetNonEnumeratedCount returned string count")

        countVal['value'] = 0

        # not possible as the array is buried under a generator
        print("""\n> [1, 2, 3, 4]/select(lambda s: s ** 2); squares/tryGetNonEnumeratedCoun(countVal)""")
        squares = [1, 2, 3, 4]/select(lambda s: s ** 2)
        count2 = squares/tryGetNonEnumeratedCount(countVal)
        print(count2, countVal['value'])
        self.assertTrue(not count2 and countVal['value'] == 0, 'tryGetNonEnumeratedCount could not get from generator')

        # Now we've gone and materialized it so we can get the count (it's actually the enumerated count)
        print("""\n> squares = [1, 2, 3, 4]/select(lambda s: s ** 2); enumeratedCount = squares/count(); squares/tryGetNonEnumeratedCoun(countVal)""")
        enumeratedCount = squares/count()
        count3 = squares/tryGetNonEnumeratedCount(countVal)
        print(count3, countVal['value'], enumeratedCount)
        self.assertTrue(count3 and countVal['value'] == enumeratedCount, 'tryGetNonEnumeratedCount could get from backup')

        # LINQ doesn't give a way to execute an operation without returning results, but JOIN provides forEach
        print("""\n> [1, 2, 3]/select(lambda s: s * s)/forEach(lambda item, idx: forEachTest.append("{0}={1}".format(idx, item)))""")
        forEachTest = []
        [1, 2, 3]/select(lambda s: s * s)/forEach(lambda item, idx: forEachTest.append("{0}={1}".format(idx, item)))
        print(forEachTest)
        self.assertListEqual(forEachTest, ["0=1", "1=4", "2=9"], "ForEach looped through iterable")

        print("\nTEST 4: Test successful")

unittest.main()
