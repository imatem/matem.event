# -*- coding: utf-8 -*-
"""Base module for unittetsing."""

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2


class EventExtenderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Prepare Zope instance by loading appropiate ZCMLs."""
        # Load ZCML
        import matem.event
        self.loadZCML(package=matem.event)

    def setUpPloneSite(self, portal):
        """Prepare a Plone instance for testing."""
        # There is no content or workflows installed by default.
        # Enable workflows
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

        # Load product profile after sample-content so definitions
        # in types/*.xml keep valid
        applyProfile(portal, 'matem.event:default')

        # Login as manager to allow object construction
        setRoles(portal, TEST_USER_ID, ['Manager'])

FIXTURE = EventExtenderLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='EventExtenderLayer:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='EventExtenderLayer:Functional')
