# The tests in test_uvcsite.py are picked up by zope.testrunner.

# When decorating a unittest.TestCase or doctest with a layer, the layer is
# used to group tests and execute setup and teardown of the grok environment
# for the test to run in.

import unittest
import doctest
import uvcsite.tests
import uvcsite.testing

from pkg_resources import resource_listdir
from zope.testing import renormalizing


browser_layer = uvcsite.testing.UVCSiteLayer(uvcsite.tests)


def suiteFromPackage(name):

    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    checker = renormalizing.RENormalizing()

    globs = {
        "layer": browser_layer
    }

    optionflags = (
        doctest.IGNORE_EXCEPTION_DETAIL +
        doctest.ELLIPSIS +
        doctest.NORMALIZE_WHITESPACE +
        doctest.REPORT_NDIFF
        )

    for filename in files:
        if filename == '__init__.py':
            continue

        test = None
        if filename.endswith('.py'):
            dottedname = f'uvcsite.tests.{name}.{filename[:-3]}'
            test = doctest.DocTestSuite(
                dottedname,
                checker=checker,
                extraglobs=globs,
                optionflags=optionflags)
        elif filename.endswith('.txt'):
            test = doctest.DocFileSuite(
                os.path.join(name, filename),
                optionflags=optionflags,
                globs=globs)
        if test is not None:
            test.layer = browser_layer
            suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in (
            "auth",
            "content"):
        suite.addTest(suiteFromPackage(name))
    return suite
