import os
import doctest
import grokcore.site.util
import transaction
import unittest
import uvcsite.app
import uvcsite.testing

from zope.testing import renormalizing
from zope.component import provideUtility
from zope.component.hooks import setSite
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer


IGNORE = {
    'fixtures',
    '__pycache__'
}


class UVCSiteLayer(ZopeFanstaticBrowserLayer):

    def create_application(self, name):
        root = self.getRootFolder()
        if name in root:
            raise KeyError('Application already exists.')
        with transaction.manager:
            grokcore.site.util.create_application(
                uvcsite.app.Uvcsite, root, name)
        app = root[name]
        setSite(app)
        return app

    def testTearDown(self):
        super().testTearDown()
        setSite()


browser_layer = UVCSiteLayer(uvcsite.browser.tests)


def suiteFromPackage(folder, module_name, layer=None):

    suite = unittest.TestSuite()
    checker = renormalizing.RENormalizing()

    globs = {
        "layer": layer
    }

    optionflags = (
        doctest.IGNORE_EXCEPTION_DETAIL +
        doctest.ELLIPSIS +
        doctest.NORMALIZE_WHITESPACE +
        doctest.REPORT_NDIFF
        )

    for subfolder in (f for f in os.scandir(folder)
                      if f.is_dir() and f.name not in IGNORE):


        for content in (f for f in os.scandir(subfolder.path) if f.is_file()):
            if content.name == '__init__.py':
                continue

            test = None
            if content.name.endswith('.py'):
                dottedname = f"{module_name}.{subfolder.name}.{content.name[:-3]}"
                test = doctest.DocTestSuite(
                    dottedname,
                    checker=checker,
                    extraglobs=globs,
                    optionflags=optionflags)
            elif content.name.endswith('.txt'):
                test = doctest.DocFileSuite(
                    content.path,
                    optionflags=optionflags,
                    globs=globs)

            if test is not None:
                if layer is not None:
                    test.layer = layer
                suite.addTest(test)

    return suite
