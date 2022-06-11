#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *


"""
Basic Single-Sequence Queries

The meat of JOIN to Python is taken up by basic query operations that everyone who works with arrays is used to: filtering elements, projecting results, slicing and skipping, and so on.
"""
class SingleSequenceTests(unittest.TestCase):
    def test(self):
        # Every lesson in queries starts with select. Select projects a function onto every entry in the enumerable.

        # 1,4,9,16,25
        print("""\n > [1, 2, 3, 4, 5]/select(lambda s: s * s)/toList()""")
        test01 = [1, 2, 3, 4, 5]/select(lambda s: s * s)/toList()
        print(test01)
        self.assertListEqual(test01, [1, 4, 9, 16, 25], 'Select squares')

        # function can take index as 2nd parameter
        print("""\n> [1, 2, 3, 4]/select(lambda s, idx: '{0}^2={1}'.format(idx + 1, s * s))/toList()""")
        test02 = [1, 2, 3, 4]/select(lambda s, idx: '{0}^2={1}'.format(idx + 1, s * s))/toList()
        print(test02)
        self.assertListEqual(test02, ["1^2=1", "2^2=4", "3^2=9", "4^2=16"], "Select with index")

        # The second step in every lesson in queries is "where."

        # 2,4,6,8
        print("""\n> [1, 2, 3, 4, 5, 6, 7, 8]/where(lambda q: q % 2 == 0)/toList()""")
        test03 = [1, 2, 3, 4, 5, 6, 7, 8]/where(lambda q: q % 2 == 0)/toList()
        print(test03)
        self.assertListEqual(test03, [2, 4, 6, 8], 'Where even')

        # function can take index as 2nd parameter
        print("""\n> [1, 2, 3, 4, 5, 6, 7, 8]/where(lambda q, idx: idx < 3)/toList()""")
        test04 = [1, 2, 3, 4, 5, 6, 7, 8]/where(lambda q, idx: idx < 3)/toList()
        print(test04)
        self.assertListEqual(test04, [1, 2, 3], 'Where with index')

        # You now know 90% of everything you'll need. But here are some more functions.

        # 3,4,5
        print("""\n> [1, 2, 3, 4, 5]/skip(2)/toList()""")
        test05 = [1, 2, 3, 4, 5]/skip(2)/toList()
        print(test05)
        self.assertListEqual(test05, [3, 4, 5], 'Skip first 2')

        # 1,2,3
        print("""\n> [1, 2, 3, 4, 5]/skipLast(2)/toList()""")
        test06 = [1, 2, 3, 4, 5]/skipLast(2)/toList()
        print(test06)
        self.assertListEqual(test06, [1, 2, 3], 'Skip last 2')

        # skip as long as condition is false, then take rest
        print("""\n> [1, 2, 3, 4, 5]/skipWhile(lambda q: q != 3)/toList()""")
        test07 = [1, 2, 3, 4, 5]/skipWhile(lambda q: q != 3)/toList()
        print(test07)
        self.assertListEqual(test07, [3, 4, 5], 'Skip until 3')

        # function can take index as 2nd parameter
        print("""\n> [1, 2, 3, 4, 5]/skipWhile(lambda q, idx: idx != 3)/toList()""")
        test08 = [1, 2, 3, 4, 5]/skipWhile(lambda q, idx: idx != 3)/toList()
        print(test08)
        self.assertListEqual(test08, [4, 5], 'SkipWhile with index')

        # 1,2
        print("""\n> [1, 2, 3, 4, 5]/take(2)/toList()""")
        test09 = [1, 2, 3, 4, 5]/take(2)/toList()
        print(test09)
        self.assertListEqual(test09, [1, 2], 'Take first 2')

        # 2,3,4
        print("""\n> [1, 2, 3, 4, 5]/take(3,1)/toList()""")
        test09skip1 = [1,2,3,4,5]/take(3,1)/toList()
        print(test09skip1)
        self.assertListEqual(test09skip1, [2, 3, 4], 'Take first 3 after skip 1')

        # Python contains a slice object, which you usualy see in the form of [1:3], [:-1], [::2], etc.
        # It's the original inspiration for C#'s range object, which is in the form 1..3, 0..^1, etc.
        # System.Linq's Take() has an overload that takes a range object, so JOIN can take a slice object.

        # 1,2 (same as take(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(None, 2))/toList()""")
        test09slice1 = [1,2,3,4,5]/take(sliceObject = slice(None, 2))/toList()
        print(test09slice1)
        self.assertListEqual(test09slice1, [1, 2], 'Take wth slice 1')

        # 2,3,4 (same as take(3,1))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(1, 4))/toList()""")
        test09slice2 = [1,2,3,4,5]/take(sliceObject = slice(1, 4))/toList()
        print(test09slice2)
        self.assertListEqual(test09slice2, [2, 3, 4], 'Take wth slice 2')

        # 3,4,5 (same as skip(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(2, None))/toList()""")
        test09slice3 = [1,2,3,4,5]/take(sliceObject = slice(2, None))/toList()
        print(test09slice3)
        self.assertListEqual(test09slice3, [3, 4, 5], 'Take wth slice 3')

        # 1,3 ([1:4] is 1,2,3,4 and then step 2)
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(0, 4, 2))/toList()""")
        test09slice4 = [1,2,3,4,5]/take(sliceObject = slice(0, 4, 2))/toList()
        print(test09slice4)
        self.assertListEqual(test09slice4, [1, 3], 'Take wth slice 4')

        # 1,2,3 (same as skipLast(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(None, -2))/toList()""")
        test09slice5 = [1,2,3,4,5]/take(sliceObject = slice(None, -2))/toList()
        print(test09slice5)
        self.assertListEqual(test09slice5, [1, 2, 3], 'Take wth slice 5')

        # 4,5 (same as takeLast(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(-2, None))/toList()""")
        test09slice6 = [1,2,3,4,5]/take(sliceObject = slice(-2, None))/toList()
        print(test09slice6)
        self.assertListEqual(test09slice6, [4, 5], 'Take wth slice 6')

        # 5,3,1 (same as reverse()/step(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(None, None, -2))/toList()""")
        test09slice7 = [1,2,3,4,5]/take(sliceObject = slice(None, None, -2))/toList()
        print(test09slice7)
        self.assertListEqual(test09slice7, [5, 3, 1], 'Take wth slice 7')

        # 4,2 (same as take(4)/reverse()/step(2))
        print("""\n> [1,2,3,4,5]/take(sliceObject = slice(3, None, -2))/toList()""")
        test09slice8 = [1,2,3,4,5]/take(sliceObject = slice(3, None, -2))/toList()
        print(test09slice8)
        self.assertListEqual(test09slice8, [4, 2], 'Take wth slice 8')

        # You might have noticed step() in the last few tests and said, hey, LINQ doesn't have that.
        # Well it's something I thought might be useful.

        # 1,3, 5 (same as take(sliceObject=slice(None,None,2)))
        print("""\n> [1,2,3,4,5]/step(2)/toList()""")
        test09step1 = [1,2,3,4,5]/step(2)/toList()
        print(test09step1)
        self.assertListEqual(test09step1, [1, 3, 5], 'Step every 2')

        # 1,4,7 (same as take(sliceObject=slice(None,None,3)))
        print("""\n> [1,2,3,4,5,6,7]/step(3)/toList()""")
        test09step2 = [1,2,3,4,5,6,7]/step(3)/toList()
        print(test09step2)
        self.assertListEqual(test09step2, [1, 4, 7], 'Step every 3')

        # 4,5
        print("""\n> [1, 2, 3, 4, 5]/takeLast(2)/toList()""")
        test10 = [1, 2, 3, 4, 5]/takeLast(2)/toList()
        print(test10)
        self.assertListEqual(test10, [4, 5], 'Take last 2')

        # Return rows until condition is true, then stop
        print("""\n> [1, 2, 3, 4, 5]/takeWhile(lambda q: q != 3)/toList()""")
        test11 = [1, 2, 3, 4, 5]/takeWhile(lambda q: q != 3)/toList()
        print(test11)
        self.assertListEqual(test11, [1, 2], 'TakeWhile not 3')

        # function can take index as 2nd parameter
        print("""\n> [1, 2, 3, 4, 5]/takeWhile(lambda q, idx: idx != 3)/toList()""")
        test12 = [1, 2, 3, 4, 5]/takeWhile(lambda q, idx: idx != 3)/toList()
        print(test12)
        self.assertListEqual(test12, [1, 2, 3], 'TakeWhile with index')

        # 1,2,3
        print("""\n> [1, 1, 2, 2, 2, 3, 3, 3, 3]/distinct()/toList()""")
        test13 = [1, 1, 2, 2, 2, 3, 3, 3, 3]/distinct()/toList()
        print(test13)
        self.assertListEqual(test13, [1, 2, 3], 'Get distinct entries')

        #  a custom equality comparer can be passed e.g. to allow comparison by key
        print("""\n> [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]/distinct(lambda q, r: q.a == r.a)""")
        test14 = (
                [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]
                /distinct(lambda q, r: q.a == r.a)
                /toList()
                )
        print(test14)
        self.assertListEqual(drain(map(lambda m: m.a, test14)), [1, 2, 3], 'Distinct with custom equality')

        # distinctBy() does its check based on a key selector function
        # (I know this is almost the same as the previous, but it was added in .Net 6)
        print("""\n> [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]/distinctBy(lambda q: q.a)""")
        test15 = (
                [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]
                /distinctBy(lambda q: q.a)
                /toList()
                )
        print(test15)
        self.assertListEqual(drain(map(lambda m: m.a, test15)), [1, 2, 3], 'Distinct by key')

        # also takes a custom equality comparer
        print("""\n> [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]/distinctBy(lambda q: q.a, lambda q, r: q % 2 == r % 2)""")
        test16 = (
            [Object(a = 1), Object(a = 1), Object(a = 2), Object(a = 2), Object(a = 3), Object(a = 3), Object(a = 3), Object(a = 1)]
            /distinctBy(lambda q: q.a, lambda q, r: q % 2 == r % 2)
            /toList()
            )
        print(test16)
        self.assertListEqual(drain(map(lambda m: m.a, test16)), [1, 2], 'Distinct by key: one even & one odd')

        # SelectMany() loops through the first level, flattens an array within that level, and returns it at the top level.

        # several examples will work with this
        numberSets = [Object(type = 'odd', numbers = [1, 3, 5]), Object(type = 'even', numbers = [2, 4, 6]), Object(type = 'prime', numbers = [2, 5, 7, 11])]

        # 1,3,5,2,4,6,2,5,7,11
        print("""\n> numberSets/selectMany(lambda q: q.numbers)/toList()""")
        test17 = numberSets/selectMany(lambda q: q.numbers)/toList()
        print(test17)
        self.assertListEqual(test17, [1, 3, 5, 2, 4, 6, 2, 5, 7, 11], 'Select many flattens inside arrays')

        # function to get iterable can take index as 2nd parameter
        print("""\n> numberSets/selectMany(lambda q, idx : map(lambda m: '{idx}: {m}'.format(m=m, idx=idx), q.numbers))/toList()""")
        test18 = numberSets/selectMany(lambda q, idx : map(lambda m: '{idx}: {m}'.format(m=m, idx=idx), q.numbers))/toList()
        print(test18)
        self.assertListEqual(test18, ["0: 1", "0: 3", "0: 5", "1: 2", "1: 4", "1: 6", "2: 2", "2: 5", "2: 7", "2: 11"], 'SelectMany with index')

        # an output function can be provided to project onto the flattened results, letting you combine parent and child
        print("""\n> numberSets/selectMany(lambda q: q.numbers, lambda s, res: "{t}: {res}".format(t=s.type, res=res))/toList()""")
        test19 = numberSets/selectMany(lambda q: q.numbers, lambda s, res: "{t}: {res}".format(t=s.type, res=res))/toList()
        print(test19)
        self.assertListEqual(test19, ["odd: 1", "odd: 3", "odd: 5", "even: 2", "even: 4", "even: 6", "prime: 2", "prime: 5", "prime: 7", "prime: 11"], 'SelectMany with output function')

        # element function can take index as 2nd parameter
        print("""\n> numberSets/selectMany(lambda q, idx: map(lambda m: "({idx}) {m}".format(m=m, idx=idx), q.numbers), lambda s, res: "{t} {res}".format(t=s.type, res=res))/toList()""")
        test20 = numberSets/selectMany(lambda q, idx: map(lambda m: "(#{idx}) {m}".format(m=m, idx=idx), q.numbers), lambda s, res: "{t} {res}".format(t=s.type, res=res))/toList()
        print(test20)
        self.assertListEqual(test20, ["odd (#0) 1", "odd (#0) 3", "odd (#0) 5", "even (#1) 2", "even (#1) 4", "even (#1) 6", "prime (#2) 2", "prime (#2) 5", "prime (#2) 7", "prime (#2) 11"], "SelectMany with index in output")

        # Cast() is impossible in Python, so cast() is just an alias for select()
        print("""\n> [1, 2, 3]/cast(lambda num: str(num))/toList()""")
        test21 = [1, 2, 3]/cast(lambda num: str(num))/toList()
        print(test21)
        self.assertListEqual(test21, ["1", "2", "3"], "Cast runs conversion function")

        # OfType() is also nonsense in Python, so this either does isinstance
        print("""\n> [2, 'two', 3, 'three', 4, 'four']/ofType(int)/toList()""")
        test22 = [2, 'two', 3, 'three', 4, 'four']/ofType(int)/toList()
        print(test22)
        self.assertListEqual(test22, [2, 3, 4], 'OfType number')

        print("\nTEST 3: Test successful")

unittest.main()
