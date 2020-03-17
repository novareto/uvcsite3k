# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import urllib
import uvc.menus.components
import uvc.menus.directives

from uvcsite.interfaces import IHomeFolder
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.component import getMultiAdapter
from megrok.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir("templates")


class PersonalPanel(uvcsite.browser.Page):
    """Page for Personal Properties
    """
    grok.name("personalpanelview")
    grok.order(35)
    grok.require("zope.View")
    grok.context(IHomeFolder)

    grok.title(u"Meine Einstellungen")
    title = u"Meine Einstellungen"
    description = u"Hier werden Einstellungen zu" " Ihrem Benutzerprofil \
        vorgenommen."

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class PersonalPanelTemplate(PageTemplate):
    grok.view(PersonalPanel)


class PersonalPanelEntry(uvc.menus.components.MenuItem):
    grok.name("personalpanelentry")
    grok.require("zope.View")
    grok.order(35)
    uvc.menus.directives.menu(
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences)

    title = "Meine Einstellungen"

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal, None)
        if None:
            return ""
        viewname = "personalpanelview"
        return urllib.parse.unquote(grok.util.url(self.request, hf, viewname))


class UserName(uvc.menus.components.MenuItem):
    grok.name("username")
    grok.title("USERSNAME")
    uvc.menus.directives.menu(
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences)
    grok.order(10)
    grok.require("zope.View")

    action = ""

    @property
    def title(self):
        return self.request.principal.title

    def url(self):
        return "#"


class MeinOrdner(uvc.menus.components.MenuItem):
    grok.context(Interface)
    grok.name("Mein Ordner")
    grok.order(20)
    grok.require("zope.View")
    uvc.menus.directives.menu(
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences)

    title = "Mein Ordner"

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal, None)
        if hf:
            return urllib.parse.unquote(grok.util.url(self.request, hf))
        return ""


class ChangePasswordMenu(uvc.menus.components.MenuItem):
    grok.context(IHomeFolder)
    #grok.require('zope.View')
    grok.order(50)
    grok.name('ChangePW')
    uvc.menus.directives.menu(
        uvcsite.browser.layout.slots.interfaces.IPersonalMenu)

    title = u"Passwort ändern"
    icon = u"fas fa-lock-open"

    def url(self):
        return self.view.url(
            IHomeFolder(self.request.principal), 'changepassword')


class Mitbenutzerverwaltung(uvc.menus.components.MenuItem):
    grok.context(IHomeFolder)
    grok.order(30)
    #grok.require("uvc.ManageCoUsers")
    grok.name("Mitbenutzerverwaltung")
    uvc.menus.directives.menu(
        uvcsite.browser.layout.slots.interfaces.IPersonalMenu)

    title = u"Mitbenutzerverwaltung"
    icon = "fas fa-users"

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal, None)
        if homeFolder:
            return str(absoluteURL(homeFolder, self.request)) + "/enms"
        return ""

