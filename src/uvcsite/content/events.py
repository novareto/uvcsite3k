# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import grok
from zope import interface
import zope.component.interfaces


class IAfterSaveEvent(zope.component.interfaces.IObjectEvent):
    "My special event"
    principal = interface.Attribute("Pincipal")


class AfterSaveEvent(zope.component.interfaces.ObjectEvent):
    grok.implements(IAfterSaveEvent)

    def __init__(self, object, request):
        self.object = object
        self.request = request
        self.principal = request.principal
