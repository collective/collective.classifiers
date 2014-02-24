from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from .utils import join_classifiers_terms


class ClassifiersVocabulary(object):
    """Vocabulary for classifiers on a content item.

    This will give terms with titles and values like:

    - Main Theme A
    - Main Theme A > Sub 1
    - Main Theme A > Sub 2
    - Main Theme B
    """
    implements(IVocabularyFactory)
    registry_name = ''

    def __call__(self, context):
        normalize = getUtility(IIDNormalizer).normalize
        registry = getUtility(IRegistry)
        classifiers = registry[self.registry_name]
        items = []
        for main, subs in classifiers.items():
            main = main.strip()
            # values and tokens need to be ascii
            normalized_main = normalize(main)
            if main:
                term = SimpleTerm(normalized_main, normalized_main, main)
                items.append(term)
            if subs is None:
                continue
            for sub in subs:
                sub = sub.strip()
                if not sub:
                    continue
                title = join_classifiers_terms(main, sub)
                # values and tokens need to be ascii
                normalized_sub = normalize(sub)
                value = join_classifiers_terms(normalized_main, normalized_sub)
                term = SimpleTerm(value, value, title)
                items.append(term)
        return SimpleVocabulary(items)


class ThemesVocabulary(ClassifiersVocabulary):
    registry_name = 'collective.classifiers.themes'


class CategoriesVocabulary(ClassifiersVocabulary):
    registry_name = 'collective.classifiers.categories'


ThemesVocabularyFactory = ThemesVocabulary()
CategoriesVocabularyFactory = CategoriesVocabulary()
