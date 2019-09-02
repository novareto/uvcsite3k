# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from megrok.pagetemplate import PageTemplate
from .interfaces import (
    IGlobalMenu,
    IPersonalPreferences,
    IDocumentActions,
    IExtraViews,
    ISpotMenu,
    IPersonalMenu,
    IQuickLinks,
    IFooter,
)
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.pagetemplate.interfaces import IPageTemplate
from uvcsite.browser.layout.menu import Menu, IMenu


grok.templatedir("templates")


class GlobalMenu(Menu):
    grok.implements(IGlobalMenu)
    grok.provides(IMenu)
    grok.name("globalmenu")


class FooterMenu(Menu):
    grok.implements(IFooter)
    grok.provides(IMenu)
    grok.name("footermenu")


class PersonalPreferences(Menu):
    grok.implements(IPersonalPreferences)
    grok.provides(IMenu)
    grok.name("personalpreferences")


class DocumentActionsMenu(Menu):
    grok.implements(IDocumentActions)
    grok.provides(IMenu)
    grok.name("documentactions")


class ExtraViews(Menu):
    grok.implements(IExtraViews)
    grok.provides(IMenu)
    grok.name("extraviews")


class SpotMenu(Menu):
    grok.implements(ISpotMenu)
    grok.provides(IMenu)
    grok.name("spotmenu")


class PersonalMenu(Menu):
    grok.implements(IPersonalMenu)
    grok.provides(IMenu)
    grok.name("personal_menu")


class QuickLinks(Menu):
    grok.implements(IQuickLinks)
    grok.provides(IMenu)
    grok.name("quicklinks")


class PersonalMenuRenderer(uvcsite.browser.layout.menu.MenuRenderer):
    grok.context(Interface)
    grok.name("personalmenu")

    bound_menus = ('personal_menu', "personalpreferences")


class GlobalMenuRenderer(uvcsite.browser.layout.menu.MenuRenderer):
    grok.context(Interface)
    grok.name("globalmenu")

    bound_menus = ("globalmenu",)


class FooterMenuRenderer(uvcsite.browser.layout.menu.MenuRenderer):
    grok.context(Interface)
    grok.name("footer")

    bound_menus = ("footermenu",)
