# -*- coding: utf-8 -*-

import grok

from zope import interface
from zope.pluggableauth import factories
from uvcsite.interfaces import IHomeFolder
from uvcsite.utils import shorties
from zope.security.interfaces import IPrincipal


@interface.implementer(IPrincipal)
class Principal(factories.Principal):

    def __repr__(self):
        return "UVCSite_Principal('%s')" % self.id

    @property
    def homefolder(self):
        return IHomeFolder(self)

    @property
    def homefolder_url(self):
        request = shorties.getRequest()
        return grok.util.url(request, self.homefolder)

    def getCoUsers(self):
        return None

    def getObjects(self):
        return None
