PROFILE_ID = 'profile-collective.classifiers:default'


def run_registry_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
