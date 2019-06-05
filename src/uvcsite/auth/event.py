import grok
import uvcsite
import zope.interface
import zope.component.interfaces

from uvcsite.auth.interfaces import ICOUser
from uvcsite.content.folderinit import createProductFolders
from uvcsite.extranetmembership.interfaces import IUserManagement
from uvcsite.interfaces import IHomeFolder
from zope.component import getUtility
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.securitypolicy.interfaces import IPrincipalRoleManager


class IUserLoggedInEvent(zope.component.interfaces.IObjectEvent):
    pass


class UserLoggedInEvent(zope.component.interfaces.ObjectEvent):
    pass


@grok.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    principal = factory.object
    createProductFolders(principal)
    homefolder = IHomeFolder(principal).homeFolder
    if not homefolder:
        return
    um = getUtility(IUserManagement)
    user = um.getUser(principal.id)
    if not user:
        return
    rollen = user['rollen']
    if user['az'] != '00':
        pid = "%s-%s" % (user['mnr'], user['az'])
    else:
        pid = user['mnr']
    if homefolder.__name__ != pid:
        for pf in homefolder.keys():
            if pf in rollen:
                prm = IPrincipalRoleManager(homefolder.get(pf))
                if prm.getSetting('uvc.Editor', pid).getName() == 'Unset':
                    prm.assignRoleToPrincipal('uvc.Editor', pid)
                    uvcsite.log(
                        'Give uvc.Editor to %s in folder %s' % (pid, pf))


@grok.subscribe(IAuthenticatedPrincipalCreated)
def applyGroups(factory):
    principal = factory.principal
    principal.groups.append('uvc.Member')
    if principal.id.count('-') >= 1:
        zope.interface.alsoProvides(principal, ICOUser)
