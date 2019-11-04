# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import uvc.menus.components

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


grok.templatedir("templates")


@implementer(IGlobalMenu)
class GlobalMenu(uvc.menus.components.Menu):
    grok.name("globalmenu")


@implementer(IFooter)
class FooterMenu(uvc.menus.components.Menu):
    grok.name("footermenu")


@implementer(IPersonalPreferences)
class PersonalPreferences(uvc.menus.components.Menu):
    grok.name("personalpreferences")


@implementer(IDocumentActions)
class DocumentActionsMenu(uvc.menus.components.Menu):
    grok.name("documentactions")


@implementer(IExtraViews)
class ExtraViews(uvc.menus.components.Menu):
    grok.name("extraviews")


@implementer(ISpotMenu)
class SpotMenu(uvc.menus.components.Menu):
    grok.name("spotmenu")


@implementer(IPersonalMenu)
class PersonalMenu(uvc.menus.components.Menu):
    grok.name("personal_menu")


@implementer(IQuickLinks)
class QuickLinks(uvc.menus.components.Menu):
    grok.name("quicklinks")


class PersonalMenuRenderer(uvc.menus.components.MenuRenderer):
    grok.context(Interface)
    grok.name("personalmenu")

    bound_menus = ('personal_menu', )


class GlobalMenuRenderer(uvc.menus.components.MenuRenderer):
    grok.context(Interface)
    grok.name("globalmenu")

    bound_menus = ("globalmenu",)


class FooterMenuRenderer(uvc.menus.components.MenuRenderer):
    grok.context(Interface)
    grok.name("footer")

    bound_menus = ("footermenu",)
