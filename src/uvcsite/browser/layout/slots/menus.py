# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok

from megrok.pagetemplate import PageTemplate
from .interfaces import (
    IGlobalMenu,
    IPersonalPreferences,
    IDocumentActions,
    IExtraViews,
    ISpotMenu,
    IPersonalMenu,
    IQuickLinks,
)
from .components import Menu
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir("templates")


class GlobalMenu(Menu):
    grok.implements(IGlobalMenu)
    grok.name("globalmenu")

from uvcsite.browser.layout.menu import Menu as NM, IMenu
class PersonalPreferences(NM):
    grok.implements(IPersonalPreferences)
    grok.provides(IMenu)
    grok.name("personalpreferences")


class DocumentActionsMenu(Menu):
    grok.implements(IDocumentActions)
    grok.name("documentactions")


class ExtraViews(Menu):
    grok.implements(IExtraViews)
    grok.context(Interface)
    grok.name("extraviews")


class SpotMenu(Menu):
    grok.implements(ISpotMenu)
    grok.name("spotmenu")


class PersonalMenu(Menu):
    grok.implements(IPersonalMenu)
    grok.context(Interface)
    grok.name("personalmenu")

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class PersonalMenuTemplate(PageTemplate):
    grok.view(PersonalMenu)


class QuickLinks(Menu):
    grok.implements(IQuickLinks)
    grok.name("quicklinks")
