import os
import unittest
import uvcsite.testing


def test_suite():
    suite = unittest.TestSuite()
    folder = os.path.dirname(__file__)
    suite.addTest(uvcsite.testing.suiteFromPackage(
        folder, 'uvcsite.browser.tests', layer=uvcsite.testing.browser_layer))
    return suite
