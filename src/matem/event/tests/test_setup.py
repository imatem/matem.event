import unittest

from matem.event.tests import base


class testInstall(base.TestCase):
    """ Test wheter the product is installed correctly
    """

    def testProductInstalled(self):
        self.failUnless(self.qi.isProductInstalled('matem.event'),
                        'matem.event is not installed')

    def testSchemaExtension(self):
        self.failUnless(self.dummyEvent.Schema().get('researchTopic') is not None,
                        'fail to append researchTopic field to Events.')


def test_suite():
    print 'test suit'
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testInstall))
    return suite
