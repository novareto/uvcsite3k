import os
import doctest
import grokcore.site.util
import transaction
import unittest
import zope.testbrowser.wsgi

from grokcore.xmlrpc.ftests.test_grok_functional import XMLRPCTestTransport
from zope.app.wsgi.testlayer import XMLRPCServerProxy
from zope.component import provideUtility
from zope.component.hooks import setSite
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer
from zope.testing import renormalizing

import uvcsite
import uvcsite.app
import uvcsite.testing


IGNORE = {
    'fixtures',
    '__pycache__'
}


class AppLayer(ZopeFanstaticBrowserLayer):

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


class BrowserLayer(AppLayer):

    def new_browser(self, url):
        return zope.testbrowser.wsgi.Browser(
            url, wsgi_app=self.make_wsgi_app())


class XMLRPC(AppLayer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transport = XMLRPCTestTransport()
        transport.wsgi_app = self.make_wsgi_app
        self.transport = transport

    def xmlrpc_server(self, url, handle_errors=False):
        server = XMLRPCServerProxy(url, transport=self.transport)
        server.handleErrors = handle_errors
        return server


application_layer = AppLayer(uvcsite)
browser_layer = BrowserLayer(uvcsite)
xmlrpc_layer = XMLRPC(uvcsite)


def suiteFromPackage(folder, module_name, layer=None):

    suite = unittest.TestSuite()
    checker = renormalizing.RENormalizing()

    optionflags = (
        doctest.IGNORE_EXCEPTION_DETAIL +
        doctest.ELLIPSIS +
        doctest.NORMALIZE_WHITESPACE +
        doctest.REPORT_NDIFF
        )

    for subfolder in os.scandir(folder):
        if not subfolder.is_dir() or subfolder.name in IGNORE:
            continue

        for f in os.scandir(subfolder.path):
            if not f.is_file():
                continue
            if f.name == '__init__.py':
                continue

            test = None
            if f.name.endswith('.py'):
                dottedname = f"{module_name}.{subfolder.name}.{f.name[:-3]}"
                test = doctest.DocTestSuite(
                    dottedname,
                    checker=checker,
                    extraglobs={
                        "layer": layer,
                        "dottedname": dottedname
                    },
                    optionflags=optionflags)
            elif f.name.endswith('.txt'):
                test = doctest.DocFileSuite(
                    f.path,
                    optionflags=optionflags,
                    globs={
                        "layer": layer,
                        "filename": f.path
                    })

            if test is not None:
                if layer is not None:
                    test.layer = layer
                suite.addTest(test)

    return suite
