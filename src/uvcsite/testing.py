import io
import base64
import grokcore.site.util
import transaction
import fanstatic

import zope.component
import zope.testbrowser.wsgi
import zope.security
import zope.authentication.interfaces

from zope.app.wsgi.testlayer import XMLRPCServerProxy
from zope.component.hooks import setSite
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer
from zope.pluggableauth.factories import Principal
from zope.publisher.browser import TestRequest, BrowserRequest

from grokcore.xmlrpc.ftests.test_grok_functional import XMLRPCTestTransport

import uvcsite
import uvcsite.app
import uvcsite.testing


class AuthenticatedRequest:

    def __init__(self, uid):
        self.request = TestRequest()
        self.principal = Principal(uid)

    def __enter__(self):
        zope.security.management.endInteraction()
        self.request.setPrincipal(self.principal)
        zope.security.management.newInteraction(self.request)
        return self.request

    def __exit__(self, *args, **kwargs):
        self.request.setPrincipal(None)
        zope.security.management.endInteraction()


class Request:

    def create_authentication_header(self, uid):
        manager = zope.component.getUtility(IUserManagement)
        credentials = manager.getUser(uid)
        return "Basic {}".format(
            base64.encodebytes(
                "{0}:{1}".format(credentials['mnr'],
                                 credentials['passwort']).encode("utf-8")
            ).decode('utf-8')
        )

    def __init__(self, uid, **kwargs):
        environ = {
            'wsgi.url_scheme': 'http',
            'QUERY_STRING': '',
            'PATH_INFO': '/',
            'SERVER_URL': 'http://localhost',
            'HTTP_HOST': 'localhost',
            'CONTENT_LENGTH': '0',
            'GATEWAY_INTERFACE': 'NovaretoTest/1.0'
        }
        environ.update(kwargs)
        environ['HTTP_AUTHORIZATION'] = self.create_authentication_header(uid)
        self.request = BrowserRequest(io.BytesIO(), environ)

    def __enter__(self):
        zope.security.management.newInteraction(self.request)
        authentication = zope.component.getUtility(
            zope.authentication.interfaces.IAuthentication)
        principal = authentication.authenticate(self.request)
        self.request.setPrincipal(principal)
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
