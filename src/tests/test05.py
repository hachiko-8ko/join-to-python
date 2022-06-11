#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *

"""
Singleton Results

Once you have a query, you might want to process that query to get a result, whether it be counting the rows, finding the min or max value, or picking the first or last. These operations will enumerate the dataset (materializing the enumerable) to find the result.
"""
class SingletonTests(unittest.TestCase):
    def test(self):
        print("""> ['loser', 'loser', 'loser', 'winner', 'loser']/elementAt(3)""")
        test01 = ['loser', 'loser', 'loser', 'winner', 'loser']/elementAt(3)
        print(test01)
        self.assertEqual(test01, 'winner', 'Element at 3rd')

        # works the same way
        print("""\n> ['loser', 'loser', 'loser', 'winner', 'loser']/elementAtOrDefault(3)""")
        test02 = ['loser', 'loser', 'loser', 'winner', 'loser']/elementAtOrDefault(3)
        print(test02)
        self.assertEqual(test02, 'winner', 'ElementAtDefault 3rd')

        # elementAt(13) would have thrown
        print("""\n> ['loser', 'loser', 'loser', 'winner', 'loser']/elementAtOrDefault(13, 'default')""")
        test03 = ['loser', 'loser', 'loser', 'winner', 'loser']/elementAtOrDefault(13, 'default')
        print(test03)
        self.assertEqual(test03, 'default', 'ElementAt with default')

        # check if all are odd
        print("""\n> [1, 3, 4, 5]/all_(lambda num: num % 2 == 1)""")
        test04 = [1, 3, 4, 5]/all_(lambda num: num % 2 == 1)
        print(test04)
        self.assertFalse(test04, 'All is false')

        # check if all are odd
        print("""\n> [1, 3, 5]/all_(lambda num: num % 2 == 1)""")
        test05 = [1, 3, 5]/all_(lambda num: num % 2 == 1)
        print(test05)
        self.assertTrue(test05, 'All is true')

        # check if index of all is less than 1 (kind of BS test)
        print("""\n> [1, 3, 5]/all_(lambda num, idx: idx < 1)""")
        test05a = [1, 3, 5]/all_(lambda num, idx: idx < 1)
        print(test05a)
        self.assertFalse(test05a, 'All is false with index')

        # does sequence have anything
        print("""\n> [1, 2, 3]/any_()""")
        test06 = [1, 2, 3]/any_()
        print(test06)
        self.assertTrue(test06, 'Any with full array')

        # Any can take a filter function, same as where(func)/any()
        print("""\n> [1, 2, 3]/any_(lambda num: num % 2 == 0)""")
        test07 = [1, 2, 3]/any_(lambda num: num % 2 == 0)
        print(test07)
        self.assertTrue(test07, 'Any with filter')

        print("""\n> [1, 3]/any_(lambda num: num % 2 == 0)""")
        test08 = [1, 3]/any_(lambda num: num % 2 == 0)
        print(test08)
        self.assertFalse(test08, 'Any with filter and no match')

        # check if index on any is greater than 10 (kind of BS test)
        print("""\n> [1, 3]/any_any(lambda num, idx: idx > 10)""")
        test08a = [1, 3]/any_(lambda num, idx: idx > 10)
        print(test08a)
        self.assertFalse(test08a, 'Any with filter and index')

        # is element in sequence
        print("""\n> [1, 2, 3]/contains(3)""")
        test09 = [1, 2, 3]/contains(3)
        print(test09)
        self.assertTrue(test09, 'Contains with match')

        # no match
        print("""\n> ["a", "b", "c"]/contains("B")""")
        test10 = ["a", "b", "c"]/contains("B")
        print(test10)
        self.assertFalse(test10, 'Contains with no match')

        # can take custom equality
        print("""\n> ["a", "b", "c"]/contains("B", lambda x, y: x.upper() == y.upper())""")
        test10a = ["a", "b", "c"]/contains("B", lambda x, y: x.upper() == y.upper())
        print(test10a)
        self.assertTrue(test10a, 'Contains with custom equality match')

        # 4
        print("""\n> [1, 2, 2, -2]/count()""")
        test11 = [1, 2, 2, -2]/count()
        print(test11)
        self.assertEqual(test11, 4, 'Count a sequence')

        # count can take a filter condition, same as where(func).count()
        print("""\n> [1, 2, 3, 4, 5, 6, 7]/count(lambda num: num % 2 == 0)""")
        test12 = [1, 2, 3, 4, 5, 6, 7]/count(lambda num: num % 2 == 0)
        print(test12)
        self.assertEqual(test12, 3, 'Count with filter')

        # longCount is the same as count, because in Python int includes large numbers
        print("""\n> ["x", "y", "z"]/longCount()""")
        test13 = ["x", "y", "z"]/longCount()
        print(test13)
        self.assertEqual(test13,  3, "LongCount a sequence")

        # also takes a filter
        print("""\n> ["x", "y", "z", "X"]/longCount(lambda q: q.lower() == "x")""")
        test14 = ["x", "y", "z", "X"]/longCount(lambda q: q.lower() == "x")
        print(14)
        self.assertEqual(test14, 2, "LongCount with filter")

        # sum the values
        print("""\n> [1, 2, 3, 4, 5]/sum_()""")
        test15 = [1, 2, 3, 4, 5]/sum_()
        print(test15)
        self.assertEqual(test15, 15, 'Sum sequence values')

        # can apply a transformation function before summing
        print("""\n> [1, 2, 3, 4, 5]/sum_(lambda q: q * 2)""")
        test16 = [1, 2, 3, 4, 5]/sum_(lambda q: q * 2)
        print(test16)
        self.assertEqual(test16, 30, 'Sum with transformation')

        # note1: throws if empty, can't divide by zero
        # note2: None are skipped, both in sum and count
        print("""\n> [1, 3, 4, 4, None]/average()""")
        test17 = [1, 3, 4, 4, None]/average()
        print(test17)
        self.assertEqual(test17, 3.0, 'Average sequence')

        # LINQ says to ignore nulls in nullable numbers, and if all are null, return null
        print("""\n> [None]/average()""")
        test17a = [None]/average()
        print(test17a)
        self.assertEqual(test17a, None, 'Average null sequence')

        print("""\n> [2, 3, 4]/first()""")
        test18 = [2, 3, 4]/first()
        print(test18)
        self.assertEqual(test18, 2, 'First in sequence')

        # can take a filter function, same as where(func).first()
        # should return 4
        print("""\n> [2, 3, 4]/first(lambda q: q > 3)""")
        test19 = [2, 3, 4]/first(lambda q: q > 3)
        print(test19)
        self.assertEqual(test19, 4, 'First with filter')

        # the filter condition can take index as a parameter (another BS test)
        print("""\n> [1, 1, 2, 3, 4]/first(lambda q, idx: idx == 3)""")
        test19a = [1, 1, 2, 3, 4]/first(lambda q, idx: idx == 3)
        print(test19a)
        self.assertEqual(test19a, 3, 'First with filter on index')

        # this will throw because there are no matches
        print("""\n> [2, 3, 4]/first(lambda q: q > 100) # will throw""")
        throw1 = False
        try:
            [2, 3, 4]/first(lambda q: q > 100)
        except EmptySequenceException:
            print("ERROR")
            throw1 = True
        self.assertTrue(throw1, 'First threw')

        # firstOrDefault will return the value provided (or Nonee) instead of throwing
        print("""\n> [2, 3, 4]/firstOrDefault(lambda q: q > 100, -1)""")
        test20 = [2, 3, 4]/firstOrDefault(lambda q: q > 100, -1)
        print(test20)
        self.assertEqual(test20, -1, 'FirstOrDefault with default')

        # also takes filter with index
        print("""\n> [1, 1, 2, 3, 4]/firstOrDefault(lambda q, idx: idx == 3)""")
        test20a = [1, 1, 2, 3, 4]/firstOrDefault(lambda q, idx: idx == 3)
        print(test20a)
        self.assertEqual(test20a, 3, 'FirstOrDefault with filter on index')

        print("""\n> []/firstOrDefault(defaultValue = -2)""")
        test21 = []/firstOrDefault(defaultValue = -2)
        print(test21)
        self.assertEqual(test21, -2, "FirstOrDefault with only default")

        # can't have first without last
        print("""\n> ['first', 'second', 'third', 'fourth', 'last']/last()""")
        test22 = ['first', 'second', 'third', 'fourth', 'last']/last()
        print(test22)
        self.assertEqual(test22, 'last', 'Last of sequence')

        # last can also take filter, same as where(func).last()
        print("""\n> ['first', 'second', 'third', 'fourth', 'last']/last(lambda q: q[0] == "f")""")
        test23 = ['first', 'second', 'third', 'fourth', 'last']/last(lambda q: q[0] == "f")
        print(test23)
        self.assertEqual(test23, 'fourth', 'Last with filter')

        # last filter also allows index
        print("""\n> ['first', 'second', 'third', 'fourth', 'last']/last(lambda q, idx: idx < 3)""")
        test23a = ['first', 'second', 'third', 'fourth', 'last']/last(lambda q, idx: idx < 3)
        print(test23a)
        self.assertEqual(test23a, 'third', 'Last with filter and index')

        # just like with first() this will throw
        print("""\n> ['first', 'second', 'third']/last(lambda q: len(q) > 100)""")
        throw2 = False
        try:
            ['first', 'second', 'third']/last(lambda q: len(q) > 100)
        except EmptySequenceException:
            print("ERROR")
            throw2 = True
        self.assertTrue(throw2, "Last throws on empty sequence")

        # doesn't throw, instead returns default
        print("""\n> ['first', 'second', 'third', 'fourth', 'last']/lastOrDefault(lambda q: q[0] == "X", "default")""")
        test24 = ['first', 'second', 'third', 'fourth', 'last']/lastOrDefault(lambda q: q[0] == "X", "default")
        print(test24)
        self.assertEqual(test24, 'default', 'LastOrDefault with default')

        # filter also allows index
        print("""\n> ['first', 'second', 'third', 'fourth', 'last']/lastOrDefault(lambda q, idx: idx < 3)""")
        test24a = ['first', 'second', 'third', 'fourth', 'last']/lastOrDefault(lambda q, idx: idx < 3)
        print(test24a)
        self.assertEqual(test24a, 'third', 'Last with filter and index')

        # just like with first, passing only default value
        print("""\n> []/lastOrDefault(defaultValue = "default")""")
        test25 = []/lastOrDefault(defaultValue = "default")
        print(test25)
        self.assertEqual(test25, 'default', 'LastOrDefault with only default')

        # returns record if there is exactly one, throwing if 0 or more than one
        print("""\n> [1]/single()""")
        test26 = [1]/single()
        print(test26)
        self.assertEqual(test26, 1, 'Single record in sequence')

        # takes a filter function, same as where(func).single()
        print("""\n> [1, 2]/single(lambda q: q % 2 == 0)""")
        test27 = [1, 2]/single(lambda q: q % 2 == 0)
        print(test27)
        self.assertEqual(test27, 2, 'Single with filter')

        # filter function can take index
        print("""\n> [1, 2]/single(lambda q, idx: idx == 0)""")
        test27a = [1, 2]/single(lambda q, idx: idx == 0) # will never have over 1
        print(test27a)
        self.assertEqual(test27a, 1, 'Single with filter and index')

        # single throws if there are multiple matches
        print("""\n> [1, 2, 3, 4]/single(lambda q: q < 3)""")
        throw4 = False
        try:
            [1, 2, 3, 4]/single(lambda q: q < 3)
        except DuplicateException:
            print("ERROR")
            throw4 = True
        self.assertTrue(throw4, 'Single throws when multiple returned')

        # Like first() and last(), single() throws on an empty sequence
        print("""\n> []/single()""")
        throw3 = False
        try:
            []/single()
        except EmptySequenceException:
            print("ERROR")
            throw3 = True
        self.assertTrue(throw3, 'Single throws on empty sequence')

        # also with filter
        print("""\n> [1, 2, 3, 4]/single(lambda q: q > 10000)""")
        throw5 = False
        try:
            [1, 2, 3, 4]/single(lambda q: q > 10000)
        except EmptySequenceException:
            throw5 = True
        self.assertTrue(throw5, 'Single throws on empty sequence with filter')

        # singleOrDefault supplies default value for empty sequence, still throws if multiple
        print("""\n> [1, 2, 3, 4]/singleOrDefault(lambda q: q > 1000, -1)""")
        test28 = [1, 2, 3, 4]/singleOrDefault(lambda q: q > 1000, -1)
        print(test28)
        self.assertEqual(test28, -1, "Default returned for singleOrDefault")

        # filter function can take index
        print("""\n> [1, 2]/singleOrDefault(lambda q, idx: idx == 0)""")
        test28a = [1, 2]/singleOrDefault(lambda q, idx: idx == 0) # will never have over 1
        print(test28a)
        self.assertEqual(test28a, 1, 'SingleOrDefault with filter and index')

        throw6 = False
        try:
            [1, 2, 3, 4]/singleOrDefault(lambda q: q % 2 == 0)
        except DuplicateException:
            print("ERROR")
            throw6 = True
        self.assertTrue(throw6, "SingleOrDefault still throws on multiple")

        # 7 is maximum
        print("""\n> [2, 3, 5, 7, 6, 4, 1]/max_()""")
        test29 = [2, 3, 5, 7, 6, 4, 1]/max_()
        print(test29)
        self.assertEqual(test29, 7, 'Max returns maximum')

        # can take a transformation function applied before maximum, same as select(func).max()
        print("""\n> [2, 3, 5, 6, 4, 1]/max_(lambda q: q * q)""")
        test30 = [2, 3, 5, 6, 4, 1]/max_(lambda q: q * q)
        print(test30)
        self.assertEqual(test30, 36, 'Max returned with function')

        # Max can take a custom comparer that returns 1 if the first value is greater, -1 is the second, else 0
        def ignoreEvenComparer(x, y):
            x = 0 if x % 2 == 0 else x
            y = 0 if y % 2 == 0 else y
            if x > y:
                return 1
            elif x < y:
                return -1
            else:
                return 0

        # max not counting evens
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/max_(lambda q: q.n, ignoreEvenComparer)""")
        test31 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/max_(lambda q: q.n, ignoreEvenComparer)
        print(test31)
        self.assertEqual(test31, 5, 'Max with custom comparer and transformation')

        print("""\n> [2, 3, 5, 6, 4, 1]/max_(comparer = ignoreEvenComparer)""")
        test32 = [2, 3, 5, 6, 4, 1]/max_(comparer = ignoreEvenComparer)
        print(test32)
        self.assertEqual(test32, 5, 'Max with custom comparer')

        # maxBy uses a key selector function, compares the keys, but returns the element
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/maxBy(lambda q: q.n)""")
        test33 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/maxBy(lambda q: q.n)
        print(test33)
        self.assertEqual(test33.n, 6, "MaxBy with key lookup")

        # maxBy also takes custom comparer
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/maxBy(lambda q: q.n, ignoreEvenComparer)""")
        test34 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/maxBy(lambda q: q.n, ignoreEvenComparer)
        print(test34)
        self.assertEqual(test34.n, 5, 'MaxBy with custom comparer')

        # 1 is minimum
        print("""\n> [2, 3, 5, 7, 6, 4, 1]/min_()""")
        test35 = [2, 3, 5, 7, 6, 4, 1]/min_()
        print(test35)
        self.assertEqual(test35, 1, 'Min returns minimum')

        # min also takes transformation function, same as select(func).min()
        print("""\n> [2, 3, 5, 6, 4]/min_(lambda q: q * q)""")
        test36 = [2, 3, 5, 6, 4]/min_(lambda q: q * q)
        print(test36)
        self.assertEqual(test36, 4, 'Min with filter')

        def ignoreEvenComparer2(x, y):
            x = 110 if x % 2 == 0 else x
            y = 110 if y % 2 == 0 else y
            if x > y:
                return 1
            elif x < y:
                return -1
            else:
                return 0

        # should be 3 (the custom comparer filters out evens)
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/min_(lambda q: q.n, ignoreEvenComparer2)""")
        test37 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/min_(lambda q: q.n, ignoreEvenComparer2)
        print(test37)
        self.assertEqual(test37, 3, "Min with custom comparer and transformation")

        print("""\n> [2, 3, 5, 6, 4]/min_(comparer = ignoreEvenComparer2)""")
        test38 = [2, 3, 5, 6, 4]/min_(comparer = ignoreEvenComparer2)
        print(test38)
        self.assertEqual(test38, 3, "Min with custom comparer only")

        # also a minBy that takes a key selector
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/minBy(lambda q: q.n)""")
        test39 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/minBy(lambda q: q.n)
        print(test39)
        self.assertEqual(test39.n, 2, "MinBy returns min with key lookup")

        # minBy also takes a custom comparer
        print("""\n> [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/minBy(lambda q: q.n, ignoreEvenComparer2)""")
        test40 = [Object(n = 2), Object(n = 3), Object(n = 5), Object(n = 6), Object(n = 4)]/minBy(lambda q: q.n, ignoreEvenComparer2)
        print(test40)
        self.assertEqual(test40.n, 3, 'MinBy with custom comparer')

        # Max_() and Min_() throw when called on an empty sequence. To handle that, I created 2 JOIN-specific methods.

        # same as defaultIfEmpty('default').max_()
        print("""\n> []/maxOrDefault(defaultValue = 'default')""")
        test41 = []/maxOrDefault(defaultValue = 'default')
        print(test41)
        self.assertEqual(test41, 'default', 'max value or default')

        # same as defaultIfEmpty('default').min()
        print("""\n> []/minOrDefault(defaultValue = 'default')""")
        test42 = []/minOrDefault(defaultValue = 'default')
        print(test42)
        self.assertEqual(test42, 'default', 'min value or default')

        # aggregate acts like reduce(), in this case tracking the max length but it could sum up the results, etc
        print("""\n> ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if len(nextItem) > len(longest) else longest)""")
        test43 = ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if len(nextItem) > len(longest) else longest)
        print(test43)
        self.assertEqual(test43, 'passionfruit', 'Aggregate with only functon')

        def countLetterN(word):
            return len([x for x in word if x == 'n'])

        # Initial value can be provided. Unlike C#, where it is the first argument, in Python it is the second, because required parameters
        # must come before optional ones.
        print("""\n> ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if countLetterN(nextItem) > countLetterN(longest) else longest, 'banana')""")
        test44 = ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if countLetterN(nextItem) > countLetterN(longest) else longest, 'banana')
        print(test44)
        self.assertEqual(test44, 'banana', 'Aggregate with initial value')

        # can take initial value and a function called upon the final result
        print("""\n> ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if len(nextItem) > len(longest) else longest, 'banana', lambda fruit: fruit.upper())""")
        test45 = ['apple', 'mango', 'orange', 'passionfruit', 'grape']/aggregate(lambda longest, nextItem: nextItem if len(nextItem) > len(longest) else longest, 'banana', lambda fruit: fruit.upper())
        print(test45)
        self.assertEqual(test45, 'PASSIONFRUIT', 'Aggregate with initial value and output function')

        print("\nTEST 5: Test successful")

unittest.main()
