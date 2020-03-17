import grok
import zope.schema
import zope.interface
import zope.component

from zope.authentication.interfaces import (
    ILogout, IUnauthenticatedPrincipal, IAuthentication)
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.location.interfaces import ILocation

from zeam.form.base import action, Fields
from uvcsite.browser import Form
from zeam.form.base.markers import SUCCESS, FAILURE
from uvcsite import uvcsiteMF as _
import uvcsite.utils.shorties
import uvcsite.auth.interfaces
from uvcsite.auth.event import UserLoggedInEvent


class ILoginForm(zope.interface.Interface):
    """A simple login form interface.
    """

    login = zope.schema.TextLine(
        title=_("Username"),
        required=True)

    password = zope.schema.Password(
        title=_("Password"),
        required=True)

    camefrom = zope.schema.TextLine(
        title=_("Origin of the request"),
        required=False)


class Login(Form):
    """A very basic implementation of a login form.
    """
    grok.title(_("Log in"))
    grok.require("zope.Public")
    grok.context(zope.interface.Interface)

    prefix = ""
    label = _("Identify yourself")
    form_name = _("Login form")

    fields = Fields(ILoginForm)
    fields['camefrom'].mode = 'hidden'
    for field in fields:
        field.prefix = ""

    @action(_("Log in"))
    def login(self):
        data, errors = self.extractData()
        if errors:
            return FAILURE
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            self.status = _("Login failed")
            return FAILURE

        self.flash(
            _("You are now logged in as ${name}",
              mapping={"name": principal.id}))

        grok.notify(UserLoggedInEvent(principal))
        camefrom = self.request.get("camefrom", None)
        if not camefrom:
            if ILocation.providedBy(principal):
                camefrom = absoluteURL(principal, self.request)
            else:
                camefrom = absoluteURL(self.context, self.request)

        self.redirect(camefrom)
        return SUCCESS


class Logout(grok.View):
    grok.context(zope.interface.Interface)
    grok.require('zope.Public')

    def update(self):
        if uvcsite.utils.shorties.isLoggedIn(self.request):
            auth = zope.component.queryUtility(IAuthentication)
            ILogout(auth).logout(self.request)

    def render(self):
        self.redirect(self.url(self.context))
