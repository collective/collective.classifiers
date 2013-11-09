# -*- coding: utf-8 -*-

from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.classifiers
        self.loadZCML(package=collective.classifiers)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.classifiers:default')
        # self.applyProfile(portal, 'collective.classifiers:testfixture')
        # Enable behavior.  In testfixture?


class FixtureWithExtraProfile(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import collective.classifiers
        self.loadZCML(package=collective.classifiers)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'plone.app.dexterity:default')
        self.applyProfile(portal, 'collective.classifiers:default')
        self.applyProfile(portal, 'collective.classifiers:testfixture')


FIXTURE = Fixture()
FIXTURE_WITH_EXTRA_PROFILE = FixtureWithExtraProfile()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.classifiers:Integration',
)
EXTRA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE_WITH_EXTRA_PROFILE,),
    name='collective.classifiers:ExtraIntegration',
)
