from plone.indexer import indexer

from .behaviors import IThemes, ICategories
from .utils import extract_all_classifiers


@indexer(IThemes)
def classifiers_themes(object):
    classifiers_themes = IThemes(object).classifiers_themes
    if classifiers_themes is None:
        return
    return extract_all_classifiers(classifiers_themes)


@indexer(ICategories)
def classifiers_categories(object):
    classifiers_categories = ICategories(object).classifiers_categories
    if classifiers_categories is None:
        return
    return extract_all_classifiers(classifiers_categories)
