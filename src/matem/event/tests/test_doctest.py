# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc
from matem.event.tests import base
import doctest
import unittest


def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='matem.event',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
