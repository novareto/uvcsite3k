# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope.interface import implementer
from zope.security.interfaces import IPrincipal
from uvcsite.auth.interfaces import IMasterUser
from uvcsite.interfaces import IHomeFolder
from zope.securitypolicy.interfaces import IPrincipalRoleMap, Allow


@implementer(uvcsite.IMyRoles)
class MyRoles(grok.Adapter):
    grok.context(IPrincipal)

    def __init__(self, principal):
        self.principal = principal
        self.homefolder = IHomeFolder(IMasterUser(self.principal)).homeFolder

    def getAllRoles(self):
        ret = []
        hfr = IPrincipalRoleMap(self.homefolder, None)
        if hfr is None:
            return ret

        masteruser = False
        for rolesetting in hfr.getRolesForPrincipal(self.principal.id):
            role, setting = rolesetting
            if 'uvc.Editor' == role and setting is Allow:
                masteruser = True
                ret.append('ENMS')
        for name, productfolder in self.homefolder.items():
            if not name.startswith('__'):
                if masteruser:
                    ret.append(name)
                else:
                    prm = IPrincipalRoleMap(productfolder)
                    for rolesetting in prm.getRolesForPrincipal(
                            self.principal.id):
                        role, setting = rolesetting
                        if 'uvc.Editor' == role and setting is Allow:
                            ret.append(name)
        return ret
