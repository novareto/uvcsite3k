import grok
import uvcsite.permissions

from uvcsite import log
from uvcsite.interfaces import IHomeFolder
from uvcsite.auth.event import IUserLoggedInEvent
from zope.securitypolicy.interfaces import IPrincipalRoleManager


#@grok.subscribe(IUserLoggedInEvent)
def applyViewContentForCoUsers(factory):
    principal = factory.object
    homefolder = IHomeFolder(principal)
    if homefolder is None:
        return
    if homefolder.__name__ != principal.id:
        hprm = IPrincipalRoleManager(homefolder)
        setting = hprm.getSetting(
            uvcsite.permissions.HomeFolderUser.name,
            principal.id).getName()
        if setting in ('Deny', 'Unset'):
            hprm.assignRoleToPrincipal(
                uvcsite.permissions.HomeFolderUser.name, principal.id)
            log('applying Role uvc.HomeFolderUser for USER %s in HOMEFOLDER %s'
                % (principal.id, homefolder.__name__))
