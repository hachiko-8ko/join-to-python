#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *

"""
Multi-Sequence Queries

These functions, which include inner joins, outer joins, concatenation, and semi-joins, compare and/or combine multiple iterables.
"""
class MultiSequenceQueryTests(unittest.TestCase):
    def test(self):

        # To be equal two sequences need to be the same length and have the same items in the same order.
        # different lengths
        print("""> [1, 2, 3]/sequenceEqual([2, 3])""")
        test01 = [1, 2, 3]/sequenceEqual([2, 3])
        print(test01)
        self.assertFalse(test01, "SequenceEqual tests length 1")

        # different lengths
        print("""\n> [1, 3]/sequenceEqual([2, 3, 1])""")
        test02 = [1, 3]/sequenceEqual([2, 3, 1])
        print(test02)
        self.assertFalse(test02, "SequenceEqual tests length 2")

        # order matters
        print("""\n> [1, 2, 3]/sequenceEqual([2, 3, 1])""")
        test03 = [1, 2, 3]/sequenceEqual([2, 3, 1])
        print(test03)
        self.assertFalse(test03, "SequenceEqual tests items")

        # this is good
        print("""\n> [1, 2, 3]/sequenceEqual([1, 2, 3])""")
        test04 = [1, 2, 3]/sequenceEqual([1, 2, 3])
        print(test04)
        self.assertTrue(test04, "SequenceEqual matches items and length")

        # with a custom equality comparer
        print("""\n> [1, 2, 3]/sequenceEqual([-2, -3], lambda x, y: abs(x) == abs(y))""")
        test05 = [1, 2, 3]/sequenceEqual([-2, -3], lambda x, y: abs(x) == abs(y))
        print(test05)
        self.assertFalse(test05, 'SequenceEqual with custom comparer tests length 1')

        # with a custom equality comparer
        print("""\n> [1, 3]/sequenceEqual([-2, -3, -1], lambda x, y: abs(x) == abs(y))""")
        test06 = [1, 3]/sequenceEqual([-2, -3, -1], lambda x, y: abs(x) == abs(y))
        print(test06)
        self.assertFalse(test06, 'SequenceEqual with custom comparer tests length 2')

        # with a custom equality comparer
        print("""\n> [1, 2, 3]/sequenceEqual([-2, -3, -1], lambda x, y: abs(x) == abs(y))""")
        test07 = [1, 2, 3]/sequenceEqual([-2, -3, -1], lambda x, y: abs(x) == abs(y))
        print(test07)
        self.assertFalse(test07, 'SequenceEqual with custom comparer tests items')

        # with a custom equality comparer
        print("""\n> [1, 2, 3]/sequenceEqual([-1, -2, -3], lambda x, y: abs(x) == abs(y))""")
        test08 = [1, 2, 3]/sequenceEqual([-1, -2, -3], lambda x, y: abs(x) == abs(y))
        print(test07)
        self.assertTrue(test08, 'SequenceEqual with custom comparer to equate absolute values')

        # 1,2,3,4
        print("""\n> [1, 2]/concat([3, 4])/toArray()""")
        test09 = [1, 2]/concat([3, 4])/toArray()
        print(test09)
        self.assertListEqual(test09, [1, 2, 3, 4], "Concat concatenates sequences")

        print("""\n> [1, 2, 3, 3, 4, 2]/union([2, 3, 4, 5, 6, 6])/toArray()""")
        test10 = [1, 2, 3, 3, 4, 2]/union([2, 3, 4, 5, 6, 6])/toArray()
        print(test10)
        self.assertListEqual(test10, [1, 2, 3, 4, 5, 6], "Union concatenates and removes duplicates")

        # custom even/odd comparer
        print("""\n> [1, 2, 3, 3, 4, 2]/union([2, 3, 4, 5, 6, 6], lambda x, y: x % 2 == y % 2)/toArray()""")
        test11 = [1, 2, 3, 3, 4, 2]/union([2, 3, 4, 5, 6, 6], lambda x, y: x % 2 == y % 2)/toArray()
        print(test11)
        self.assertListEqual(test11, [1, 2], 'union with custom comparer to match evens/odds')

        # does a union on keys returned by key selector function, returning the items
        print("""\n> [Object(x = 1), Object(x = 2), Object(x = 3), Object(x = 3), Object(x = 4), Object(x = 2)]/unionBy([Object(x = 2), Object(x = 3), Object(x = 4), Object(x = 5), Object(x = 6), Object(x = 1)], lambda q: q.x)/toArray()""")
        test12 = [Object(x = 1), Object(x = 2), Object(x = 3), Object(x = 3), Object(x = 4), Object(x = 2)]/unionBy([Object(x = 2), Object(x = 3), Object(x = 4), Object(x = 5), Object(x = 6), Object(x = 1)], lambda q: q.x)/toArray()
        print(test12)
        # cheat here. this works because there's only one key per object. We won't be able to do this cheat in a moment.
        self.assertEqual(str(test12), """[{'x': 1}, {'x': 2}, {'x': 3}, {'x': 4}, {'x': 5}, {'x': 6}]""", "unionBy returns one item for each unique key")

        # custom even/odd comparer
        print("""\n> [Object(x = 1), Object(x = 2), Object(x = 3), Object(x = 3), Object(x = 4), Object(x = 2)]/unionBy([Object(x = 2), Object(x = 3), Object(x = 4), Object(x = 5), Object(x = 6), Object(x = 1)], lambda q: q.x, lambda x, y: x % 2 == y % 2)/toArray()""")
        test13 = [Object(x = 1), Object(x = 2), Object(x = 3), Object(x = 3), Object(x = 4), Object(x = 2)]/unionBy([Object(x = 2), Object(x = 3), Object(x = 4), Object(x = 5), Object(x = 6), Object(x = 1)], lambda q: q.x, lambda x, y: x % 2 == y % 2)/toArray()
        print(test13)
        self.assertEqual(str(test13), """[{'x': 1}, {'x': 2}]""", "unionBy returns one item for each unique key")

        # deduped records that are in both sequence
        print("""\n> ['A', 'A', 'C', 'Q', 'B', 'D', 'X']/intersect(['W', 'A', 'C', 'B', 'M'])/toArray()""")
        test14 = ['A', 'A', 'C', 'Q', 'B', 'D', 'X']/intersect(['W', 'A', 'C', 'B', 'M'])/toArray()
        print(test14)
        self.assertListEqual(test14, ["A", "C", "B"], "Intersection returns set result of items in 2 sequences")

        # can take a custom equality
        print("""\n> ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersect(['Watermelon', 'Avocado', 'Cucumber', 'Berry', 'Mango', 'b-wrong'], lambda x, y: x[0] == y[0])/toArray()""")
        test14a = ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersect(['Watermelon', 'Avocado', 'Cucumber', 'Berry', 'Mango', 'b-wrong'], lambda x, y: x[0] == y[0])/toArray()
        print(test14a)
        self.assertListEqual(test14a, ["Apple", "Canteloupe", "Banana"], "Intersection with custom equality")

        # find deduped keys that are in both sequences and return first item for each (redundant with the previous but it's in .net 6)
        print("""\n> ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersectBy(['Watermelon', 'Avocado', 'Cucumber', 'Berry', 'Mango', 'b-wrong'], lambda q: q[0])/toArray()""")
        test15 = ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersectBy(['Watermelon', 'Avocado', 'Cucumber', 'Berry', 'Mango', 'b-wrong'], lambda q: q[0])/toArray()
        print(test15)
        self.assertListEqual(test15, ["Apple", "Canteloupe", "Banana"], "intersectBy returns intersection by key selected")

        # custom equality comparer
        print("""\n> ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersectBy(['watermelon', 'avocado', 'cucumber', 'Berry', 'mango'], lambda q: q[0], lambda x, y: x.lower() == y.lower())/toArray()""")
        test16 = ['Apple', 'Artichoke', 'Canteloupe', 'Quince', 'Banana', 'Date', 'Xigua']/intersectBy(['watermelon', 'avocado', 'cucumber', 'Berry', 'mango'], lambda q: q[0], lambda x, y: x.lower() == y.lower())/toArray()
        print(test16)
        self.assertListEqual(test16, ["Apple", "Canteloupe", "Banana"])

        # deduped items from first not in second
        # note how the name had to be adjusted. "except" is already used in Python to define catch blocks. It's not allowed to use it anyway else.
        print("""\n> [2.0, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]/except_([2.2])/toArray()""")
        test17 = [2.0, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]/except_([2.2])/toArray()
        print(test17)
        self.assertListEqual(test17, [2.0, 2.1, 2.3, 2.4, 2.5], 'Except removes items from second sequence')

        # custom equality comparer
        print("""\n> [Object(a=2.0), Object(a=2.0), Object(a=2.1), Object(a=2.2), Object(a=2.3), Object(a=2.4), Object(a=2.5)]/except_([Object(a=2.2)], lambda q, r: q.a == r.a)/toArray()""")
        test18 = [Object(a=2.0), Object(a=2.0), Object(a=2.1), Object(a=2.2), Object(a=2.3), Object(a=2.4), Object(a=2.5)]/except_([Object(a=2.2)], lambda q, r: q.a == r.a)/toArray()
        print(test18)
        self.assertEqual(drain(map(lambda m: m.a, test18)), [2, 2.1, 2.3, 2.4, 2.5], 'Except with custom equality')

        # exceptBy returns exception by key selector
        print("""\n> [Object(a=2.0), Object(a=2.0), Object(a=2.1), Object(a=2.2), Object(a=2.3), Object(a=2.4), Object(a=2.5)]/exceptBy([Object(a=2.2)], lambda q: q.a)/toArray()""")
        test19 = [Object(a=2.0), Object(a=2.0), Object(a=2.1), Object(a=2.2), Object(a=2.3), Object(a=2.4), Object(a=2.5)]/exceptBy([Object(a=2.2)], lambda q: q.a)/toArray()
        print(test19)
        self.assertEqual(drain(map(lambda m: m.a, test19)), [2, 2.1, 2.3, 2.4, 2.5], 'ExceptBy uses key selector')

        # custom equality to make all evens and all odds look the same
        print("""\n> [Object(a=1), Object(a=1), Object(a=2), Object(a=3), Object(a=4), Object(a=5)]/exceptBy([Object(a=2)], lambda q: q.a, lambda q, r: q % 2 == r % 2)/toArray()""")
        test20 = [Object(a=1), Object(a=1), Object(a=2), Object(a=3), Object(a=4), Object(a=5)]/exceptBy([Object(a=2)], lambda q: q.a, lambda q, r: q % 2 == r % 2)/toArray()
        print(test20)
        self.assertEqual(drain(map(lambda m: m.a, test20)), [1], 'ExceptBy with custom equality')

        # Anyone with SQL experience should know what an Inner Join is.
        # An inner join matches every item in the first sequence with every item in the second sequence by matching keys, and returns those records where the key match is true, both in the same row
        # The LINQ join requires you to send two sequences, a key selector for sequence 1, a key selector for sequence 2, and an output projection function to produce the rows to return.

        # joining on first letter, returning left first letter and right full word
        print("""\n> ["Apricot", "Banana", "Cucumber"]/join(["Apple", "Canteloupe Island", "Durian", "b-wrong", "Avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: "{0} is for {1}".format(l[0], r))/toArray()""")
        test21 = ["Apricot", "Banana", "Cucumber"]/join(["Apple", "Canteloupe Island", "Durian", "b-wrong", "Avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: "{0} is for {1}".format(l[0], r))/toArray()
        print(test21)
        self.assertListEqual(test21, ["A is for Apple", "A is for Avocado", "C is for Canteloupe Island"], 'Join combines two sequences row-wise')

        # can take a custom equality comparer
        print("""\n> ["Apricot", "Banana", "Cucumber"]/join(["apple", "canteloupe Island", "durian", "avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: "{0} is for {1}".format(l[0], r), comparer = lambda x, y: x.lower() == y.lower())/toArray()""")
        test22 = ["Apricot", "Banana", "Cucumber"]/join(["apple", "canteloupe Island", "durian", "avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: "{0} is for {1}".format(l[0], r), comparer = lambda x, y: x.lower() == y.lower())/toArray()
        print(test22)
        self.assertListEqual(test22, ["A is for apple", "A is for avocado", "C is for canteloupe Island"], 'Join can take custom equality')

        # In LINQ's join, the output function is required. In JOIN, you can ignore it. If you do so, simple tuples are returned.
        print("""\n> ["Apricot", "Banana"]/join(["apple", "Canteloupe Island", "Durian", "Avocado"], lambda l: l[0], lambda r: r[0], comparer = lambda x, y: x.lower() == y.lower())/toArray()""")
        test23 = ["Apricot", "Banana"]/join(["apple", "Canteloupe Island", "Durian", "Avocado"], lambda l: l[0], lambda r: r[0], comparer = lambda x, y: x.lower() == y.lower())/toArray()
        print(test23)
        # Tuples are value types so this works
        self.assertListEqual( test23, [("Apricot","apple"),("Apricot","Avocado")], 'Join() with tuple output')

        # to test some of these we need to convert the object (a reference type, which isn't equal to an identical object) into tuple (a
        # value type, which is equal to an identical object)
        def makeTuple(obj):
            try: return (obj.l, obj.r)
            except: pass
            try: return (obj.l, None)
            except: pass
            try: return (None, obj.r)
            except: pass

        # LINQ does not provide an outer join operator. It can be done (in a truly ugly way) in the query syntax, but not in fluent methods
        # but JOIN does have an outer join
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["Berry", "Watermelon", "Avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: Object(l=l, r=r))/toArray()""")
        test24 = ["Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["Berry", "Watermelon", "Avocado"], lambda l: l[0], lambda r: r[0], lambda l, r: Object(l=l, r=r))/toArray()
        print(test24)
        self.assertListEqual(drain(map(makeTuple, test24)), [("Apple", "Avocado"), ("Apricot", "Avocado"), ("Banana", "Berry"),("Canteloupe", None)], 'outerJoin matching Join() syntax')

        # default tuple output from join() is also here
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["Berry", "Watermelon", "Avocado", "Apple"], lambda l: l[0], lambda r: r[0])/toArray()""")
        test25 = ["Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["Berry", "Watermelon", "Avocado", "Apple"], lambda l: l[0], lambda r: r[0])/toArray()
        print(test25)
        self.assertListEqual(test25, [("Apple","Avocado"),("Apple","Apple"),("Apricot","Avocado"),("Apricot","Apple"),("Banana","Berry"),("Canteloupe",None)], 'outerJoin with tuple output')

        # custom equality
        print("""\n> ["Apple", "Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["berry", "watermelon", "avocado", "apple"], lambda l: l[0], lambda r: r[0], lambda l, r: Object(l=l,r=r), lambda x, y: x.lower() == y.lower())/toArray()""")
        test26 = ["Apple", "Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["berry", "watermelon", "avocado", "apple"], lambda l: l[0], lambda r: r[0], lambda l, r: Object(l=l,r=r), lambda x, y: x.lower() == y.lower())/toArray()
        print(test26)
        self.assertListEqual(drain(map(makeTuple, test26)), [("Apple","avocado"),("Apple","apple"),("Apple","avocado"),("Apple","apple"),("Apricot","avocado"),("Apricot","apple"),("Banana","berry"),("Canteloupe", None)], 'outerJoin with custom equality')

        # custom equality and tuple output
        print("""\n> ["Apple", "Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["berry", "watermelon", "avocado", "apple"], lambda l: l[0], lambda r: r[0], comparer = lambda x, y: x.lower() == y.lower())/toArray()""")
        test27 = ["Apple", "Apple", "Apricot", "Banana", "Canteloupe"]/outerJoin(["berry", "watermelon", "avocado", "apple"], lambda l: l[0], lambda r: r[0], comparer = lambda x, y: x.lower() == y.lower())/toArray()
        print(test27)
        self.assertListEqual(test27, [("Apple","avocado"),("Apple","apple"),("Apple","avocado"),("Apple","apple"),("Apricot","avocado"),("Apricot","apple"),("Banana","berry"),("Canteloupe",None)], 'outerJoin with custom equality and tuple output')

        # The join() in LINQ is kind of a pain. I always find myself wondering what are the inputs, which is the first, which is the second,
        # why did they use 'inner' and 'outer' for things that aren't inner or outer, etc. I keep having to google it. So JOIN contains a
        # friendly version that combines two key selectors and custom equality into a single function.

        # join on first letter and return objects
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/innerJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()""")
        test28 = ["Apple", "Apricot", "Banana", "Canteloupe"]/innerJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()
        print(test28)
        self.assertListEqual(drain(map(makeTuple,test28)), [("Apple","Avocado"),("Apricot","Avocado"),("Banana","Berry")], "Basic innerJoin helper")

        # returns tuples, output function is optional
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/innerJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0])/toArray()""")
        test29 = ["Apple", "Apricot", "Banana", "Canteloupe"]/innerJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0])/toArray()
        print(test29)
        self.assertListEqual(test29, [("Apple","Avocado"),("Apricot","Avocado"),("Banana","Berry")], 'InnerJoin helper with tuple output')

        # there's also a left outer join
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/leftJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()""")
        test30 = ["Apple", "Apricot", "Banana", "Canteloupe"]/leftJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()
        print(test30)
        self.assertListEqual(drain(map(makeTuple, test30)), [("Apple","Avocado"),("Apricot","Avocado"),("Banana","Berry"),("Canteloupe", None)], 'LeftJoin helper')

        # also allows tuple output
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/leftJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0])/toArray()""")
        test31 = ["Apple", "Apricot", "Banana", "Canteloupe"]/leftJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0])/toArray()
        print(test31)
        self.assertListEqual(test31, [("Apple","Avocado"),("Apricot","Avocado"),("Banana","Berry"),("Canteloupe",None)], 'LeftJoin helper with tuple output')

        # there's also a right outer join
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/rightJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()""")
        test32 = ["Apple", "Apricot", "Banana", "Canteloupe"]/rightJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()
        print(test32)
        self.assertListEqual(drain(map(makeTuple, test32)), [("Banana","Berry"),(None,"Watermelon"),("Apple","Avocado"),("Apricot","Avocado")], 'RightJoin helper')

        # there's also a full outer join
        print("""\n> ["Apple", "Apricot", "Banana", "Canteloupe"]/fullJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()""")
        test33 = ["Apple", "Apricot", "Banana", "Canteloupe"]/fullJoin(["Berry", "Watermelon", "Avocado"], lambda l, r: l[0] == r[0], lambda l, r: Object(l=l,r=r))/toArray()
        print(test33)
        self.assertListEqual(drain(map(makeTuple, test33)), [("Apple","Avocado"),("Apricot","Avocado"),("Banana","Berry"),("Canteloupe", None),(None,"Watermelon")], 'FullJoin helper')

        # the join collection isn't complete without a cross join
        print("""\n> [2, 3]/crossJoin([5, 6], lambda l, r: Object(l=l,r=r))/toArray()""")
        test34 = [2, 3]/crossJoin([5, 6], lambda l, r: Object(l=l,r=r))/toArray()
        print(test34)
        self.assertListEqual(drain(map(makeTuple, test34)), [(2,5),(2,6),(3,5),(3,6)], 'CrossJoin helper')

        # GroupJoin is a weird one that sounds like another custom method, but this one comes from Microsoft. A group join is like
        # a combination of outer join and half a groupBy. The left and right side are joined and then the right side is grouped on
        # the joining key. If nothing is on the right, the group list is empty

        # join on first letters and group right
        print("""\n> ['Apple', 'Banana', 'Apple', 'Canteloupe']/groupJoin(['Average', 'Alphabet', 'Cartographer', 'c-wrong'], lambda q: q[0], lambda q: q[0], lambda word, alsoMatching: Object(word=word, alsoMatching=alsoMatching))/toArray()""")
        test35 = ['Apple', 'Banana', 'Apple', 'Canteloupe']/groupJoin(['Average', 'Alphabet', 'Cartographer', 'c-wrong'], lambda q: q[0], lambda q: q[0], lambda word, alsoMatching: Object(word=word, alsoMatching=alsoMatching))/toArray()
        print(test35)
        # This one is ROUGH. The anonymous objects have multiple keys, which are in random order.
        self.assertEqual(len(test35), 4, 'GroupJoin joins and groups: length')
        self.assertEqual(len(drain(filter(lambda x: x.word == 'Apple', test35))), 2, 'GroupJoin joins and groups: Apple')
        self.assertEqual(len(drain(filter(lambda x: x.word == 'Banana', test35))), 1, 'GroupJoin joins and groups: Banana')
        self.assertEqual(len(drain(filter(lambda x: x.word == 'Canteloupe', test35))), 1, 'GroupJoin joins and groups: Canteloupe')
        self.assertListEqual((test35/first(lambda q: q.word == 'Apple')).alsoMatching, ["Average","Alphabet"], 'GroupJoin joins and groups: Group side 1')
        self.assertListEqual((test35/first(lambda q: q.word == 'Canteloupe')).alsoMatching, ["Cartographer"], 'GroupJoin joins and groups: Group side 2')
        self.assertListEqual((test35/first(lambda q: q.word == 'Banana')).alsoMatching, [], 'GroupJoin joins and groups: Group side 3')

        # can take a custom equality
        print("""\n> ['Apple', 'Banana', 'Apple', 'Canteloupe']/groupJoin(['average', 'Alphabet', 'cartographer'], lambda q: q[0], lambda q: q[0], lambda word, alsoMatching: Object(word=word, alsoMatching=alsoMatching), comparer = lambda x, y: x.lower() == y.lower())/toArray()""")
        test36 = ['Apple', 'Banana', 'Apple', 'Canteloupe']/groupJoin(['average', 'Alphabet', 'cartographer'], lambda q: q[0], lambda q: q[0], lambda word, alsoMatching: Object(word=word, alsoMatching=alsoMatching), comparer = lambda x, y: x.lower() == y.lower())/toArray()
        print(test36)
        self.assertListEqual((test36/first(lambda q: q.word == 'Apple')).alsoMatching, ["average","Alphabet"], 'Group join with custom equality to ignore case 1')
        self.assertListEqual((test36/first(lambda q: q.word == 'Canteloupe')).alsoMatching, ["cartographer"], 'Group join with custom equality to ignore case 2')

        # There's already a zip() but this one is deferred.
        # This will return 3 tuples, [1,5], [2,6], and [3,7], one from each sequence in order
        print("""\n> [1, 2, 3, 4]/zip_([5, 6, 7])/toArray()""")
        test37 = [1, 2, 3, 4]/zip_([5, 6, 7])/toArray()
        print(test37)
        self.assertListEqual(test37, [(1,5),(2,6),(3,7)], 'Zip two sequences into a sequence of tuples')

        # can zip a third tuple
        print("""\n> [1, 2, 3, 4]/zip_([5, 6, 7], [8, 9, 10, 11])/toArray()""")
        test38 = [1, 2, 3, 4]/zip_([5, 6, 7], [8, 9, 10, 11])/toArray()
        print(test38)
        self.assertListEqual(test38, [(1,5,8),(2,6,9),(3,7,10)], 'Zip three sequences')

        # in place of the third tuple you can send a function that combines the first 2
        print("""\n> [1, 2, 3, 4]/zip_([5, 6, 7], lambda x, y: x * y)/toArray()""")
        test39 = [1, 2, 3, 4]/zip_([5, 6, 7], lambda x, y: x * y)/toArray()
        print(test39)
        self.assertListEqual(test39, [(1,5,5),(2,6,12),(3,7,21)], 'Zip two sequences and a virtual sequence')

        print("\nTEST 6: Test successful")

unittest.main()
