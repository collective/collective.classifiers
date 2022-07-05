# -*- coding: utf-8 -*-

import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.classifiers.testing import INTEGRATION_TESTING
from collective.classifiers.testing import EXTRA_INTEGRATION_TESTING


def normalize_keys(keys):
    # Some keys have Chinese characters that gets passed through a normalizer.
    # The Plone 6 normalizer is a bit nicer.
    new_keys = []
    for key in keys:
        new_keys.append(
            key.replace("6c498bed", "yi-yu").replace("6f228a9e", "han-yu")
        )
    return new_keys


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
        self.portal.invokeFactory('TestContainer', 'container', title=u"Container 1")
        self.container = self.portal.container

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
        # Some Chinese characters.
        keys = normalize_keys(keys)
        self.assertIn('air > non-ascii-yi-yu-han-yu-hanyu', keys)
        self.assertIn('yi-yu', keys)
        self.assertIn('yi-yu > 123', keys)

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
        keys = normalize_keys(keys)
        self.assertIn('yi-yu-han-yu-hanyu', keys)

    def test_none_categories_vocabulary(self):
        # None as value should be fine.
        registry = getUtility(IRegistry)
        classifiers = registry['collective.classifiers.categories']
        self.assertEqual(classifiers['Product'], ())
        # Explicitly set to None, which happens when you edit it, but
        # apparently not when you leave the values empty in xml.
        classifiers['Product'] = None

        # Now try the vocabulary again.
        util = getUtility(IVocabularyFactory, name='collective.classifiers.categories')
        vocab = util(self.portal)
        term = vocab.getTermByToken('product')
        self.assertEqual(term.value, 'product')
        self.assertEqual(term.token, 'product')
        self.assertEqual(term.title, u'Product')

        # Check the keys (well, the values of the vocabularies).
        keys = vocab.by_value.keys()
        self.assertTrue(len(keys) >= 5)
        self.assertTrue('product' in keys)

    def test_themes_behavior_direct_access(self):
        self.assertEqual(self.container.classifiers_themes, [])
        self.container.classifiers_themes = ['Water > Drinking']
        self.assertEqual(self.container.classifiers_themes, ['Water > Drinking'])

    def test_themes_behavior_adapter_access(self):
        from ..behaviors import IThemes
        wrapped = IThemes(self.container)
        self.assertEqual(wrapped.classifiers_themes, [])
        wrapped.classifiers_themes = ['Water > Drinking']
        self.assertEqual(wrapped.classifiers_themes, ['Water > Drinking'])

    def test_categories_behavior_direct_access(self):
        self.assertEqual(self.container.classifiers_categories, [])
        self.container.classifiers_categories = ['Report > Technical']
        self.assertEqual(self.container.classifiers_categories, ['Report > Technical'])

    def test_categories_behavior_adapter_access(self):
        from ..behaviors import ICategories
        wrapped = ICategories(self.container)
        self.assertEqual(wrapped.classifiers_categories, [])
        wrapped.classifiers_categories = ['Report > Technical']
        self.assertEqual(wrapped.classifiers_categories, ['Report > Technical'])

    def test_themes_indexer(self):
        from ..indexers import classifiers_themes
        indexer = classifiers_themes(self.container)
        self.assertEqual(indexer(), [])
        self.container.classifiers_themes = ['Water > Drinking']
        self.assertEqual(indexer(), ['Water', 'Water > Drinking'])
        self.container.classifiers_themes = [
            'Water > Drinking', 'Water > Underground']
        self.assertEqual(indexer(), ['Water', 'Water > Drinking',
                                     'Water > Underground'])
        # Create an item.
        self.container.invokeFactory('TestItem', 'item', title=u"Item 1")
        # The item is in the catalog:
        self.assertEqual(len(self.portal.portal_catalog(
            portal_type='TestItem')), 1)
        # The item should inherit the themes of its parent for
        # indexing, so it should not be found when querying the
        # catalog for a theme.
        self.assertEqual(len(self.portal.portal_catalog(
            classifiers_themes='Water > Drinking')), 1)
        item = self.container.item
        indexer = classifiers_themes(item)
        self.assertEqual(indexer(), None)

    def test_categories_indexer(self):
        from ..indexers import classifiers_categories
        indexer = classifiers_categories(self.container)
        self.assertEqual(indexer(), [])
        self.container.classifiers_categories = ['Report > Technical']
        self.assertEqual(indexer(), ['Report', 'Report > Technical'])
        self.container.classifiers_categories = [
            'Report > Technical', 'Report > Management']
        self.assertEqual(indexer(), ['Report', 'Report > Management',
                                     'Report > Technical'])
        # Create an item.
        self.container.invokeFactory('TestItem', 'item', title=u"Item 1")
        # The item is in the catalog:
        self.assertEqual(len(self.portal.portal_catalog(
            portal_type='TestItem')), 1)
        # The item should inherit the categories of its parent for
        # indexing, so it should not be found when querying the
        # catalog for a theme.
        self.assertEqual(len(self.portal.portal_catalog(
            classifiers_categories='Report > Technical')), 1)
        item = self.container.item
        indexer = classifiers_categories(item)
        self.assertEqual(indexer(), None)

    def test_collection_with_themes(self):
        self.portal.invokeFactory('Collection', 'collection', title='My Collection')
        collection = self.portal.collection
        query = [{
            'i': 'classifiers_themes',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'water',
        }]
        collection.setQuery(query)
        # There are no containers mathing the query yet.
        self.assertEqual(len(collection.results()), 0)

        # water should find water > underground
        self.container.classifiers_themes = ['water > underground']
        self.container.reindexObject()
        self.assertEqual(len(collection.results()), 1)
        self.assertEqual(collection.results()[0].Title(), "Container 1")

        # Specialize the query to water > drinking
        query = [{
            'i': 'classifiers_themes',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'water > drinking',
        }]
        collection.setQuery(query)
        self.assertEqual(len(collection.results()), 0)

        # Make the container match.
        self.container.classifiers_themes = ['water > drinking']
        self.container.reindexObject()
        self.assertEqual(len(collection.results()), 1)
        self.assertEqual(collection.results()[0].Title(), "Container 1")

    def test_collection_with_categories(self):
        self.portal.invokeFactory('Collection', 'collection', title='My Collection')
        collection = self.portal.collection
        query = [{
            'i': 'classifiers_categories',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'report',
        }]
        collection.setQuery(query)
        # There are no containers mathing the query yet.

        self.assertEqual(len(collection.results()), 0)

        # report should find report > management
        self.container.classifiers_categories = ['report > management']
        self.container.reindexObject()
        self.assertEqual(len(collection.results()), 1)
        self.assertEqual(collection.results()[0].Title(), "Container 1")

        # Specialize the query to report > technical
        query = [{
            'i': 'classifiers_categories',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'report > technical',
        }]
        collection.setQuery(query)
        self.assertEqual(len(collection.results()), 0)

        # Make the container match.
        self.container.classifiers_categories = ['report > technical']
        self.container.reindexObject()
        self.assertEqual(len(collection.results()), 1)
        self.assertEqual(collection.results()[0].Title(), "Container 1")
