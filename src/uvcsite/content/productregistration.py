# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import logging
import zope.security

from uvcsite.content.directive import productfolder
from uvcsite.content.interfaces import IProductRegistration
from uvcsite.content.meta import default_name
from uvcsite.interfaces import IHomeFolder
from uvcsite.interfaces import IHomeFolderManager
from zope.component import getMultiAdapter, getAdapters, getUtility
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.publisher.interfaces.http import IHTTPRequest
from zope.security.interfaces import IPrincipal


def getAllProductRegistrations():
    request = zope.security.management.getInteraction().participations[0]
    principal = request.principal
    return sorted(getAdapters((principal, request), IProductRegistration),
                  key=lambda k: grok.order.bind().get(k[0][0]))


def getProductRegistrations():
    request = zope.security.management.getInteraction().participations[0]
    principal = request.principal
    rc = []
    for key, value in getAdapters((principal, request), IProductRegistration):
        if value.available():
            rc.append((key, value))
    return sorted(rc, key=lambda k: grok.order.bind().get(k[1]))


@implementer(IProductRegistration)
class ProductRegistration(grok.MultiAdapter):
    grok.adapts(IPrincipal, IHTTPRequest)
    grok.baseclass()
    icon = None

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request
        self.title = grok.title.bind().get(self)
        self.name = grok.name.bind().get(self)
        self.description = grok.description.bind().get(self)

    @property
    def folderURI(self):
        if not self.productfolder:
            return
        pfn = grok.name.bind(get_default=default_name).get(self.productfolder)
        return pfn.capitalize()

    @property
    def linkname(self):
        return self.title

    @property
    def rolename(self):
        return self.title

    @property
    def productfolder(self):
        pfolder = productfolder.bind().get(self)
        if pfolder:
            return resolve(pfolder)

    def invalidRole(self):
        my_roles = uvcsite.IMyRoles(self.principal).getAllRoles()
        if not self.folderURI in my_roles:
            return True
        return False

    def available(self):
        if self.invalidRole():
            return False
        return True

    def action(self):
        return "%s/%s/@@add" % (
            uvcsite.getHomeFolderUrl(self.request), self.folderURI)

    @property
    def inNav(self):
        return self.available()

    @property
    def asRole(self):
        return self.available()

    def createInProductFolder(self):
        homefolder = IHomeFolder(self.principal).homeFolder
        if not homefolder:
            utility = getUtility(IHomeFolderManager)
            utility.assignHomeFolder(uvcsite.IMasterUser(self.principal).id)
        if self.folderURI and not self.folderURI in homefolder.keys():
            pf = self.productfolder
            homefolder[self.folderURI] = pf()
            uvcsite.log(
                'Add Productfolders %s to Homefolder: %s' % (
                    self.folderURI, self.principal.id), severity=logging.DEBUG)
