import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-collective.classifiers:default'
logger = logging.getLogger('collective.classifiers')


def run_registry_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def fix_catalog_values(context):
    # Note: reindexing the indexes is not enough, as the wrong values
    # are still in the brains.
    indexes = ['classifiers_themes', 'classifiers_categories']
    logger.info("Fixing catalog values for fields %r", indexes)
    catalog = getToolByName(context, 'portal_catalog')
    count = 0
    for brain in catalog():
        for field in indexes:
            if getattr(brain, field):
                logger.debug("Reindexing %s", brain.getPath())
                obj = brain.getObject()
                obj.reindexObject(idxs=indexes)
                count += 1
                break

    logger.info("Done fixing catalog values. %d values recalculated.", count)
