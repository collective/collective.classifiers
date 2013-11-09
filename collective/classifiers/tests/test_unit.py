# -*- coding: utf-8 -*-

import unittest

from collective.classifiers import utils


class UtilsTestCase(unittest.TestCase):

    def test_join_classifiers_terms(self):
        fun = utils.join_classifiers_terms
        self.assertEqual(fun('a', 'b'), 'a > b')
        self.assertEqual(fun(u'a', u'b'), u'a > b')
        self.assertEqual(fun(u'\xeb', u'\xeb'), u'\xeb > \xeb')
        # If our splitter is in the input, we replace it:
        self.assertEqual(fun('sneaky > with splitter', 'b'),
                         'sneaky SPLITTER with splitter > b')
        self.assertEqual(fun('', ''), '')
        self.assertEqual(fun(None, None), 'None > None')
        self.assertEqual(fun(0, 1), '0 > 1')
        # spaces are stripped
        self.assertEqual(fun(' a   ', ' '), 'a')
        self.assertEqual(fun(' ', ' b '), 'b')

    def test_split_classifiers_term(self):
        fun = utils.split_classifiers_term
        self.assertEqual(fun('a'), ['a'])
        self.assertEqual(fun('a b'), ['a b'])
        self.assertEqual(fun('a > b'), ['a', 'b'])
        self.assertEqual(fun('a >> b'), ['a >> b'])
        # Only one split is supported:
        self.assertEqual(fun('a > b > c'), ['a', 'b > c'])
        # We do not convert to integers or stuff like that:
        self.assertEqual(fun('0 > None'), ['0', 'None'])
        # Unicode should be no problem:
        self.assertEqual(fun(u'a > b'), [u'a', u'b'])
        self.assertEqual(fun(u'\xeb > \xeb'), [u'\xeb', u'\xeb'])
        # We currently do not try to revert our replacement of the
        # splitter, otherwise we would need to first check if the
        # replacement is in the original string and replace that too
        # and we just do not want to bother with that:
        self.assertEqual(fun('sneaky SPLITTER  > b'),
                         ['sneaky SPLITTER ', 'b'])

    def test_extract_all_classifiers(self):
        fun = utils.extract_all_classifiers
        self.assertEqual(fun([]), [])
        self.assertEqual(fun(['main']),
                         ['main'])
        self.assertEqual(fun(['main > sub 1']),
                         ['main', 'main > sub 1'])
        self.assertEqual(fun(['main > sub 1', 'main > sub 2']),
                         ['main', 'main > sub 1', 'main > sub 2'])
        self.assertEqual(fun(['main > sub 2', 'main > sub 1']),
                         ['main', 'main > sub 1', 'main > sub 2'])
        self.assertEqual(fun([u'main > sub 1']),
                         [u'main', u'main > sub 1'])
        self.assertEqual(fun([u'Main \xeb > sub \xeb']),
                         [u'Main \xeb', u'Main \xeb > sub \xeb'])

    def test_extract_sub_classifiers(self):
        fun = utils.extract_sub_classifiers
        self.assertEqual(fun([]), [])
        self.assertEqual(fun(['main']),
                         ['main'])
        self.assertEqual(fun(['main > sub 1']),
                         ['main > sub 1'])
        self.assertEqual(fun(['main > sub 1', 'main > sub 2']),
                         ['main > sub 1', 'main > sub 2'])
        self.assertEqual(fun(['main > sub 2', 'main > sub 1']),
                         ['main > sub 1', 'main > sub 2'])
        self.assertEqual(fun([u'main > sub 1']),
                         [u'main > sub 1'])
        self.assertEqual(fun([u'Main \xeb > sub \xeb']),
                         [u'Main \xeb > sub \xeb'])
