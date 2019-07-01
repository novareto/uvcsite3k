# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import urllib

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


class PersonalPanelEntry(uvcsite.browser.layout.menu.MenuItem):
    grok.name("personalpanelentry")
    grok.require("zope.View")
    grok.context(Interface)
    grok.order(35)

    grok.title(u"Meine Einstellungen")
    title = u"Meine Einstellungen"
    grok.adapts(
        Interface,
        Interface,
        Interface,
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences,
    )

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal)
        viewname = "personalpanelview"
        return urllib.parse.unquote(grok.util.url(self.request, hf, viewname))


class UserName(uvcsite.browser.layout.menu.MenuItem):
    grok.name("username")
    grok.title("USERSNAME")
    grok.context(Interface)
    grok.adapts(
        Interface,
        Interface,
        Interface,
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences,
    )
    grok.order(10)
    grok.require("zope.View")
    action = ""

    @property
    def title(self):
        return self.request.principal.title

    def url(self):
        return "#"


class MeinOrdner(uvcsite.browser.layout.menu.MenuItem):
    grok.context(Interface)
    grok.name("Mein Ordner")
    grok.title("Mein Ordner")
    grok.adapts(
        Interface,
        Interface,
        Interface,
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences,
    )
    grok.order(20)
    grok.require("zope.View")
    title = u"Mein Ordner"

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal)
        return urllib.parse.unquote(grok.util.url(self.request, hf))



class Mitbenutzerverwaltung(uvcsite.browser.layout.menu.MenuItem):
    grok.context(IHomeFolder)
    grok.name("Mitbenutzerverwaltung")
    grok.adapts(
        Interface,
        Interface,
        Interface,
        uvcsite.browser.layout.slots.interfaces.IPersonalPreferences,
    )
    grok.order(30)
    grok.require("uvc.ManageCoUsers")
    title = u"Mitbenutzerverwaltung"

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal)
        return str(absoluteURL(homeFolder, self.request)) + "/enms"
