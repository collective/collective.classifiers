from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides

from . import _


class IThemes(model.Schema):

    classifiers_themes = schema.List(
        title=_(u'Themes'),
        value_type=schema.Choice(
            vocabulary='collective.classifiers.themes'),
        required=False,
        default=[],
        )


class ICategories(model.Schema):

    classifiers_categories = schema.List(
        title=_(u'Categories'),
        value_type=schema.Choice(
            vocabulary='collective.classifiers.categories'),
        required=False,
        default=[],
        )

alsoProvides(IThemes, IFormFieldProvider)
alsoProvides(ICategories, IFormFieldProvider)
