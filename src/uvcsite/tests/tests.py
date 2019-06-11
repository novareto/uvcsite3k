# The tests in test_uvcsite.py are picked up by zope.testrunner.

# When decorating a unittest.TestCase or doctest with a layer, the layer is
# used to group tests and execute setup and teardown of the grok environment
# for the test to run in.

import unittest
import doctest

import uvcsite.tests
import uvcsite.testing
from zope.testing import renormalizing


browser_layer = uvcsite.testing.UVCSiteLayer(uvcsite.tests)


def test_suite():
    suite = unittest.TestSuite()
    test = doctest.DocTestSuite(
        "uvcsite.tests.auth",
        checker=renormalizing.RENormalizing(),
        extraglobs={"layer": browser_layer},
        optionflags=(
            doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE + doctest.REPORT_NDIFF
        ),
    )
    test.layer = browser_layer
    suite.addTest(test)
    return suite
