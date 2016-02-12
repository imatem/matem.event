# -*- coding: utf-8 -*-
""""Setup/installation tests for this package."""

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from matem.event.config import PROJECTNAME
from matem.event.testing import INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName


import unittest2 as unittest


class TestInstallation(unittest.TestCase):
    """Test installation of matem.event into Plone."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if product is installed in portal_quickinstaller."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled(PROJECTNAME))

    def test_uninstall(self):
        """Test if product is cleanly uninstalled."""
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts([PROJECTNAME])
        self.assertFalse(installer.isProductInstalled(PROJECTNAME))

    # extenders/event.py
    # def test_extenders_registered(self):
    #     """Test if schema extenders are registered."""
    #     reg_adapters = self.portal.getSiteManager().registeredAdapters()
    #     adapters = [a for a in reg_adapters if a.provided == ISchemaModifier]
    #     self.assertEqual(len(adapters), 1)

    # def testSchemaExtension(self):
    #     self.failUnless(
    #         self.dummyEvent.Schema().get('researchTopic') is not None,
    #         'fail to append researchTopic field to Events.')
