import unittest
import uvcsite.content.components
import uvcsite.interfaces
import uvcsite.testing
import uvcsite.homefolder.homefolder
import zope.securitypolicy.settings
import zope.component

from grokcore.component.testing import grok_component, grok
from uvcsite.tests import fixtures
from zope.pluggableauth.factories import Principal
from uvcsite.interfaces import IHomeFolder


class TestAuthPlugin(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def test_plugins_presence(self):
        from uvcsite.auth.cookies import CookiesCredentials
        from uvcsite.auth.handler import UVCAuthenticator
        from zope.component import queryUtility
        from zope.authentication.interfaces import IAuthentication
        from zope.pluggableauth.plugins import httpplugins

        # We're testing the local utilities.
        self.layer.create_application('app')
        
        auth = queryUtility(IAuthentication)
        self.assertIsNotNone(auth)

        plugins = list(auth.getCredentialsPlugins())
        self.assertTrue(len(plugins) == 2)
        self.assertEqual(plugins[0][0], 'cookies')
        self.assertTrue(isinstance(plugins[0][1], CookiesCredentials))
        self.assertEqual(plugins[1][0], 'Zope Realm Basic-Auth')
        self.assertTrue(isinstance(
            plugins[1][1], httpplugins.HTTPBasicAuthCredentialsPlugin))

        plugins = list(auth.getAuthenticatorPlugins())
        self.assertTrue(len(plugins) == 1)
        self.assertEqual(plugins[0][0], 'principals')
        self.assertTrue(isinstance(plugins[0][1], UVCAuthenticator))


class TestLogin(unittest.TestCase):
    layer = uvcsite.testing.browser_layer

    def setUp(self):
        grok('uvcsite.tests.fixtures.usermanagement')
        grok_component('Index', fixtures.views.MinimalAppIndex)

    def test_unauthorized(self):
        app = self.layer.create_application('app')
        browser = self.layer.new_browser('http://localhost/app')

        self.assertFalse('dolmen.authcookie' in browser.cookies)
        self.assertEqual(browser.url,
                         ('http://localhost/app/@@login?camefrom='
                          'http%3A%2F%2Flocalhost%2Fapp%2F%40%40index'))

    def test_login(self):
        app = self.layer.create_application('app')
        browser = self.layer.new_browser('http://localhost/app/@@login', handle_errors=False)

        # Filling up the form.
        form = browser.getForm()
        login = form.getControl(name='login')
        login.value = "0101010001"
        password = form.getControl(name='password')
        password.value = "passwort"

        # Press login
        # We are redirected AND logged in.
        form.submit(name='action.log-in')
        self.assertTrue('dolmen.authcookie' in browser.cookies)
        self.assertEqual(browser.url, "http://localhost/app")


class TestAuthEvents(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        grok('uvcsite.tests.fixtures.usermanagement')

    def test_auth_event(self):
        class F:
            def __init__(self, p):
                self.object = p
        self.layer.create_application('app')
        principal = Principal('0101010001')
        homefolder = IHomeFolder(principal, None)
        self.assertEqual(homefolder, None)
        from uvcsite.auth.event import applyPermissionsForExistentCoUsers
        applyPermissionsForExistentCoUsers(F(principal))
        homefolder = IHomeFolder(principal)
        from uvcsite.homefolder.homefolder import HomeFolder
        self.assertTrue(isinstance(homefolder, HomeFolder))
        self.assertEqual(str(homefolder), '<Homefolder for 0101010001>')
