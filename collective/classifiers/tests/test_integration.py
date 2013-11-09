# -*- coding: utf-8 -*-

import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.classifiers.testing import INTEGRATION_TESTING
from collective.classifiers.testing import EXTRA_INTEGRATION_TESTING


class IntegrationTestCase(unittest.TestCase):
    # This does NOT have the testfixture profile installed.
    layer = INTEGRATION_TESTING

    def test_themes_vocabulary(self):
        portal = self.layer['portal']
        util = getUtility(IVocabularyFactory, name='collective.classifiers.themes')
        vocab = util(portal)
        self.assertRaises(LookupError, vocab.getTerm, 'water > drinking')
        self.assertEqual(len(vocab.by_token), 0)

    def test_categories_vocabulary(self):
        portal = self.layer['portal']
        util = getUtility(IVocabularyFactory, name='collective.classifiers.categories')
        vocab = util(portal)
        self.assertRaises(LookupError, vocab.getTerm, 'water > drinking')
        self.assertEqual(len(vocab.by_token), 0)


class ExtraIntegrationTestCase(unittest.TestCase):
    # This has the testfixture profile installed.
    layer = EXTRA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('TestItem', 'item', title=u"Item 1")
        self.item = self.portal.item

    def test_themes_vocabulary(self):
        util = getUtility(IVocabularyFactory, name='collective.classifiers.themes')
        vocab = util(self.portal)
        term = vocab.getTerm('water > drinking')
        self.assertEqual(term.value, 'water > drinking')
        self.assertEqual(term.token, 'water > drinking')
        self.assertEqual(term.title, u'Water > Drinking')
        term = vocab.getTermByToken('water > drinking')
        self.assertEqual(term.value, 'water > drinking')
        self.assertEqual(term.token, 'water > drinking')
        self.assertEqual(term.title, u'Water > Drinking')

        # Check the keys (well, the values of the vocabularies).
        keys = vocab.by_value.keys()
        self.assertTrue(len(keys) >= 5)
        self.assertTrue('water' in keys)
        self.assertTrue('water > drinking' in keys)
        self.assertTrue('air' in keys)
        # Some Chinese characters:
        self.assertTrue('air > non-ascii-6c498bed-6f228a9e-hanyu' in keys)
        self.assertTrue('6c498bed' in keys)
        self.assertTrue('6c498bed > 123' in keys)

    def test_categories_vocabulary(self):
        util = getUtility(IVocabularyFactory, name='collective.classifiers.categories')
        vocab = util(self.portal)
        term = vocab.getTerm('report > technical')
        self.assertEqual(term.value, 'report > technical')
        self.assertEqual(term.token, 'report > technical')
        self.assertEqual(term.title, u'Report > Technical')
        term = vocab.getTermByToken('report > technical')
        self.assertEqual(term.value, 'report > technical')
        self.assertEqual(term.token, 'report > technical')
        self.assertEqual(term.title, u'Report > Technical')

        # Check the keys (well, the values of the vocabularies).
        keys = vocab.by_value.keys()
        self.assertTrue(len(keys) >= 5)
        self.assertTrue('product' in keys)
        self.assertTrue('report' in keys)
        self.assertTrue('report > management' in keys)
        self.assertTrue('report > technical' in keys)
        # This is a Chinese one, that gets passed through a normalizer.
        self.assertTrue('6c498bed-6f228a9e-hanyu' in keys)

    def test_themes_behavior_direct_access(self):
        self.assertEqual(self.item.classifiers_themes, [])
        self.item.classifiers_themes = ['Water > Drinking']
        self.assertEqual(self.item.classifiers_themes, ['Water > Drinking'])

    def test_themes_behavior_adapter_access(self):
        from ..behaviors import IThemes
        wrapped = IThemes(self.item)
        self.assertEqual(wrapped.classifiers_themes, [])
        wrapped.classifiers_themes = ['Water > Drinking']
        self.assertEqual(wrapped.classifiers_themes, ['Water > Drinking'])

    def test_categories_behavior_direct_access(self):
        self.assertEqual(self.item.classifiers_categories, [])
        self.item.classifiers_categories = ['Report > Technical']
        self.assertEqual(self.item.classifiers_categories, ['Report > Technical'])

    def test_categories_behavior_adapter_access(self):
        from ..behaviors import ICategories
        wrapped = ICategories(self.item)
        self.assertEqual(wrapped.classifiers_categories, [])
        wrapped.classifiers_categories = ['Report > Technical']
        self.assertEqual(wrapped.classifiers_categories, ['Report > Technical'])

    def test_themes_indexer(self):
        from ..indexers import classifiers_themes
        indexer = classifiers_themes(self.item)
        self.assertEqual(indexer(), [])
        self.item.classifiers_themes = ['Water > Drinking']
        self.assertEqual(indexer(), ['Water', 'Water > Drinking'])
        self.item.classifiers_themes = [
            'Water > Drinking', 'Water > Underground']
        self.assertEqual(indexer(), ['Water', 'Water > Drinking',
                                     'Water > Underground'])

    def test_categories_indexer(self):
        from ..indexers import classifiers_categories
        indexer = classifiers_categories(self.item)
        self.assertEqual(indexer(), [])
        self.item.classifiers_categories = ['Report > Technical']
        self.assertEqual(indexer(), ['Report', 'Report > Technical'])
        self.item.classifiers_categories = [
            'Report > Technical', 'Report > Management']
        self.assertEqual(indexer(), ['Report', 'Report > Management',
                                     'Report > Technical'])

    def test_collection_with_themes(self):
        self.portal.invokeFactory('Collection', 'collection', title='My Collection')
        collection = self.portal.collection
        query = [{
            'i': 'classifiers_themes',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'water',
        }]
        collection.setQuery(query)
        # There are no items mathing the query yet.
        self.assertEqual(len(collection.getQuery()), 0)

        # water should find water > underground
        self.item.classifiers_themes = ['water > underground']
        self.item.reindexObject()
        self.assertEqual(len(collection.getQuery()), 1)
        self.assertEqual(collection.getQuery()[0].Title(), "Item 1")

        # Specialize the query to water > drinking
        query = [{
            'i': 'classifiers_themes',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'water > drinking',
        }]
        collection.setQuery(query)
        self.assertEqual(len(collection.getQuery()), 0)

        # Make the item match.
        self.item.classifiers_themes = ['water > drinking']
        self.item.reindexObject()
        self.assertEqual(len(collection.getQuery()), 1)
        self.assertEqual(collection.getQuery()[0].Title(), "Item 1")

    def test_collection_with_categories(self):
        self.portal.invokeFactory('Collection', 'collection', title='My Collection')
        collection = self.portal.collection
        query = [{
            'i': 'classifiers_categories',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'report',
        }]
        collection.setQuery(query)
        # There are no items mathing the query yet.
        self.assertEqual(len(collection.getQuery()), 0)

        # report should find report > management
        self.item.classifiers_categories = ['report > management']
        self.item.reindexObject()
        self.assertEqual(len(collection.getQuery()), 1)
        self.assertEqual(collection.getQuery()[0].Title(), "Item 1")

        # Specialize the query to report > technical
        query = [{
            'i': 'classifiers_categories',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'report > technical',
        }]
        collection.setQuery(query)
        self.assertEqual(len(collection.getQuery()), 0)

        # Make the item match.
        self.item.classifiers_categories = ['report > technical']
        self.item.reindexObject()
        self.assertEqual(len(collection.getQuery()), 1)
        self.assertEqual(collection.getQuery()[0].Title(), "Item 1")
