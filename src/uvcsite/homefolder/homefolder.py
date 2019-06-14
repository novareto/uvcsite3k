# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from persistent import Persistent

import grok
import uvcsite.interfaces
from uvcsite.auth.interfaces import IMasterUser
from uvcsite.content.interfaces import IProductFolder
from uvcsite.interfaces import IHomeFolder, IHomeFolderManager

from zope import component
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.component import getUtilitiesFor
from zope.container.contained import Contained
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.security.interfaces import IPrincipal
from zope.securitypolicy.interfaces import IPrincipalRoleManager


@implementer(IHomeFolder)
class HomeFolder(grok.Container):

    def values(self):
        for key, value in self.items():
            if not key.startswith('__'):            
                yield value


class Members(grok.Container):
    pass


class PortalMembership(grok.Adapter):
    grok.provides(IHomeFolderManager)
    grok.context(uvcsite.interfaces.IUVCSite)

    owner_roles = [u'uvc.User', u'uvc.Editor', u'uvc.MasterUser']
    content_factory = HomeFolder

    @property
    def container(self):
        return self.context['members']

    def create(self, uid):
        home = self.container[uid] = self.content_factory()
        principal_roles = IPrincipalRoleManager(home)
        for role in self.owner_roles:
            principal_roles.assignRoleToPrincipal(role, uid)
        return home

    def __delitem__(self, uid):
        del self.container[uid]

    def __getitem__(self, uid):
        if uid in self.container:
            return self.container[uid]
        if uid not in self.container:
            return self.create(uid)
        raise KeyError('Unknown homefolder.')

    def get(self, uid, default=None):
        try:
            return self[uid]
        except KeyError:
            return default


@implementer(IHomeFolder)
class HomeFolderForPrincipal(grok.Adapter):
    grok.context(IPrincipal)

    def __init__(self, principal):
        self.principal = IMasterUser(principal)

    homeFolder = property(lambda self: getHomeFolder(self.principal))
