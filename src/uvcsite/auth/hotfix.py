import grok

from uvcsite import log
from uvcsite.interfaces import IHomeFolder
from uvcsite.auth.event import IUserLoggedInEvent
from zope.securitypolicy.interfaces import IPrincipalRoleManager


class AccessHomeFolder(grok.Permission):
    grok.name('uvc.AccessHomeFolder')


class HomeFolderUser(grok.Role):
    grok.name('uvc.HomeFolderUser')
    grok.permissions('uvc.AccessHomeFolder', )


@grok.subscribe(IUserLoggedInEvent)
def applyViewContentForCoUsers(factory):
    principal = factory.object
    homefolder = IHomeFolder(principal).homeFolder
    if not homefolder:
        return
    if homefolder.__name__ != principal.id:
        hprm = IPrincipalRoleManager(homefolder)
        setting = hprm.getSetting('uvc.HomeFolderUser', principal.id).getName()
        if setting in ('Deny', 'Unset'):
            hprm.assignRoleToPrincipal('uvc.HomeFolderUser', principal.id)
            log('applying Role uvc.HomeFolderUser for USER %s in HOMEFOLDER %s'
                % (principal.id, homefolder.__name__))
