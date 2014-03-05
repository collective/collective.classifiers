from plone.indexer import indexer
from zope.interface import Interface

from .behaviors import IThemes, ICategories
from .utils import extract_all_classifiers


@indexer(Interface)
def classifiers_themes(object):
    wrapper = IThemes(object, None)
    if wrapper is None:
        return
    classifiers_themes = wrapper.classifiers_themes
    if classifiers_themes is None:
        return
    return extract_all_classifiers(classifiers_themes)


@indexer(Interface)
def classifiers_categories(object):
    wrapper = ICategories(object, None)
    if wrapper is None:
        return
    classifiers_categories = wrapper.classifiers_categories
    if classifiers_categories is None:
        return
    return extract_all_classifiers(classifiers_categories)
