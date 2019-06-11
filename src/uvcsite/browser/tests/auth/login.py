"""
    >>> from grokcore.component.testing import grok
    >>> grok('uvcsite.browser.tests.fixtures.usermanagement')
    >>> grok(__name__)


Do a functional doctest test on the app.
========================================

Let's first create an instance of Uvcsite at the top level:

    >>> app = layer.create_application('app')
    >>> app
    <uvcsite.app.Uvcsite object at ...>


   Let's look if we have our authenticate infrastucture
----------------------------------------------------

   >>> from zope.component import getUtility
   >>> from zope.authentication.interfaces import IAuthentication

   >>> auth = getUtility(IAuthentication)
   >>> print(auth)
   <zope.pluggableauth.authentication.PluggableAuthentication object at ...>

   >>> for plugin in auth.getCredentialsPlugins():
   ...     print(plugin)
   ('cookies', <uvcsite.auth.cookies.CookiesCredentials object at 0...)
   ('Zope Realm Basic-Auth', <zope.pluggableauth.plugins.httpplugins.HTTPBasicAuthCredentialsPlugin object at 0...)

   >>> for plugin in auth.getAuthenticatorPlugins():
   ...     print(plugin)
   ('principals', <uvcsite.auth.handler.UVCAuthenticator object at 0...>)


Provide an simple Index View where we can demonstrate the login stuff



Only Authorized people should get access
----------------------------------------

   >>> from zope.testbrowser.browser import Browser
   >>> browser = Browser(wsgi_app=layer.make_wsgi_app())
   >>> browser.handleErrors = True

This means if we open the index page. We get redirected
to the login page.


   >>> browser.open('http://localhost/app')
   >>> browser.url
   'http://localhost/app/@@login?camefrom=http%3A%2F%2Flocalhost%2Fapp%2F%40%40index'

   >>> 'dolmen.authcookie' in browser.cookies
   False

Now we are at the Login Page

   >>> form = browser.getForm()
   >>> login = form.getControl(name='login')
   >>> login.value = "0101010001"

   >>> password = form.getControl(name='password')
   >>> password.value = "passwort"

   >>> came_from = form.getControl(name='camefrom')
   >>> came_from.value = 'http://localhost/app'

   >>> form.submit(name='action.log-in')

   >>> 'dolmen.authcookie' in browser.cookies
   True

   >>> print(browser.url)
   http://localhost/app
"""

import grok
import uvcsite.permissions
from zope.interface import Interface


class IndexPage(grok.View):
    grok.name("index")
    grok.context(Interface)
    grok.require('zope.View')

    def render(self):
        return "Hallo Welt"
