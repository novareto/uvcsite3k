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
from zope.interface import Interface, implementer
from zope.pagetemplate.interfaces import IPageTemplate
from uvcsite.browser.layout.menu import Menu, IMenu


grok.templatedir("templates")


@implementer(IGlobalMenu)
class GlobalMenu(Menu):
    grok.name("globalmenu")


@implementer(IFooter)
class FooterMenu(Menu):
    grok.name("footermenu")


@implementer(IPersonalPreferences)
class PersonalPreferences(Menu):
    grok.name("personalpreferences")


@implementer(IDocumentActions)
class DocumentActionsMenu(Menu):
    grok.name("documentactions")


@implementer(IExtraViews)
class ExtraViews(Menu):
    grok.name("extraviews")


@implementer(ISpotMenu)
class SpotMenu(Menu):
    grok.name("spotmenu")


@implementer(IPersonalMenu)
class PersonalMenu(Menu):
    grok.name("personal_menu")


@implementer(IQuickLinks)
class QuickLinks(Menu):
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
