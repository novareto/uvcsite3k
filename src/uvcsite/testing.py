import grokcore.site.util
import transaction
import zope.testbrowser.wsgi
import zope.security

from zope.app.wsgi.testlayer import XMLRPCServerProxy
from zope.component.hooks import setSite
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer
from zope.pluggableauth.factories import Principal
from zope.publisher.browser import TestRequest

from grokcore.xmlrpc.ftests.test_grok_functional import XMLRPCTestTransport

import uvcsite
import uvcsite.app
import uvcsite.testing


class AuthenticatedRequest:

    def __init__(self, uid):
        self.request = TestRequest()
        self.principal = Principal(uid)

    def __enter__(self):
        self.request.setPrincipal(self.principal)
        zope.security.management.newInteraction(self.request)
        return self.request

    def __exit__(self, *args, **kwargs):
        self.request.setPrincipal(None)
        zope.security.management.endInteraction()


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

    def new_browser(self, url, handle_errors=True):
        browser = zope.testbrowser.wsgi.Browser(
            url, wsgi_app=self.make_wsgi_app())
        browser.handleErrors = handle_errors
        return browser


class XMLRPCLayer(AppLayer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transport = XMLRPCTestTransport()
        transport.wsgi_app = self.make_wsgi_app
        self.transport = transport

    def xmlrpc_server(self, url, handle_errors=True):
        server = XMLRPCServerProxy(url, transport=self.transport)
        server.handleErrors = handle_errors
        return server


application_layer = AppLayer(uvcsite)
browser_layer = BrowserLayer(uvcsite)
xmlrpc_layer = XMLRPCLayer(uvcsite)
