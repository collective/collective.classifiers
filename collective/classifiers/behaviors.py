from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides

from . import _


class IThemes(model.Schema):

    classifiers_themes = schema.List(
        title=_(u'Themes'),
        description=_(u"Select one or more subjects that match this objects "
                       "content to classify it for search in other parts of "
                       "the site. Themes are specific to a website's "
                       "purpose."),
        value_type=schema.Choice(
            vocabulary='collective.classifiers.themes'),
        required=False,
        default=[],
        )


class ICategories(model.Schema):

    classifiers_categories = schema.List(
        title=_(u'Categories'),
        description=_(u"The category classifies the meta type of information this "
                       "content contains and could be seen as different "
                       "sections on the site, for example Q&A, legal, or "
                       "support pages. Categories are more generic and "
                       "can be found under the same name (like support) "
                       "on many different websites."),
        value_type=schema.Choice(
            vocabulary='collective.classifiers.categories'),
        required=False,
        default=[],
        )

alsoProvides(IThemes, IFormFieldProvider)
alsoProvides(ICategories, IFormFieldProvider)
