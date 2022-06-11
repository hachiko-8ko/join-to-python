#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0,'..')

from join_to_python import *
from AnonymousObject import *

"""
Conversions

These methods are used to convert enumerables into ordinary objects: lists, dicts, sets, defaultdict(list)s
"""
class ConversionTests(unittest.TestCase):
    def test(self):
        # an extremely redundant example ... makes a list
        test01 = [1, 3, 5]/toList()
        print("""\n [1, 3, 5].toList()""")
        print(test01)
        self.assertTrue(test01[0] == 1 and test01[1] == 3 and test01[2] == 5, 'Array is created by ToList()')

        # toList() and toArray() are the same
        test02 = [1, 3, 5]/toArray()
        print("""\n> [1, 3, 5]/toArray()""")
        print(test02)
        self.assertTrue(test02[0] == 1 and test02[1] == 3 and test02[2] == 5, 'List is created')

        # produces a dict where keys are Bob and Carol and the values are the object e.g. { name: 'Bob', wins: 20 }
        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: q.name)""")
        test03 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: q.name)
        print(test03)
        self.assertTrue(test03['Bob'].wins == 20, 'Object dictionary is created')

        # produces {"Bob":20,"Carol":34}
        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: q.name, lambda q: q.wins)""")
        test04 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: q.name, lambda q: q.wins)
        print(test04)
        self.assertTrue(test04['Bob'] == 20, 'Number dictionary is created')

        # Python has no problem with objects as dict keys
        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: Object(name = q.name))""")
        test05 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: Object(name = q.name))
        print(test05)
        self.assertTrue(len(test05) == 2 and [x for x in test05.items() if x[0].name == 'Carol'][0][1].wins == 34, 'Object dictionary is created with object key')

        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: q.name, lambda q: q.wins)""")
        test06 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34)]/toDictionary(lambda q: Object(name = q.name), lambda q: q.wins)
        print(test06)
        self.assertTrue(len(test06) == 2 and [x for x in test06.items() if x[0].name == 'Carol'][0][1] == 34, 'Number dictionary is created with object key')

        # Dicts do not allow multiple values for a key, so toLookup() products defaultdict(list), which does
        # When you call append() on a lookup, it appends the value instead of overwriting it.
        # Creates a lookup with name as key, helpful when names are duplicated
        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34), Object(name = 'Carol', wins = 10)]/toLookup(lambda q: q.name)""")
        test07 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34), Object(name = 'Carol', wins = 10)]/toLookup(lambda q: q.name)
        print(test07)
        self.assertTrue(len(test07) == 2 and len(test07['Carol']) == 2 and len([x for x in test07['Carol'] if x.wins == 10]) == 1, 'Lookup is created')

        # Creates a lookup with name as key and wins as value
        print("""\n> [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34), Object(name = 'Carol', wins = 10)]/toLookup(lambda q: q.name, lambda q: q.wins)""")
        test08 = [Object(name = 'Bob', wins = 20), Object(name = 'Carol', wins = 34), Object(name = 'Carol', wins = 10)]/toLookup(lambda q: q.name, lambda q: q.wins)
        print(test08)
        self.assertTrue(len(test08) == 2 and len(test08['Carol']) == 2 and len([x for x in test08['Carol'] if x == 10]) == 1, 'Lookup is created with element function')

        # produces set of its unique values
        print("""\n> [1, 2, 2, 3, 4, 1]/toHashSet()""")
        test09 = [1, 2, 2, 3, 4, 1]/toHashSet()
        print(test09)
        self.assertTrue(len(test09) == 4 and 1 in test09 and 2 in test09 and 3 in test09 and 4 in test09, 'Set is created')

        print("\nTEST 2: Test successful")

unittest.main()
