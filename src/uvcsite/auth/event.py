import grok
import uvcsite
import zope.interface
import zope.component.interfaces
import uvcsite.auth.interfaces

from uvcsite.extranetmembership.interfaces import IUserManagement
from uvcsite.interfaces import IHomeFolder
from zope.component import getUtility
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from uvcsite.interfaces import IHomeFolderManager
from uvcsite.auth.interfaces import IMasterUser


class IUserLoggedInEvent(zope.component.interfaces.IObjectEvent):
    pass


@zope.interface.implementer(IUserLoggedInEvent)
class UserLoggedInEvent(zope.component.interfaces.ObjectEvent):
    pass


@grok.subscribe(IAuthenticatedPrincipalCreated)
def applyGroups(factory):
    principal = factory.principal
    principal.groups.append('uvc.Member')
    if principal.id.count('-') >= 1:
        zope.interface.alsoProvides(principal, uvcsite.auth.interfaces.ICOUser)


@grok.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    site = grok.getSite()
    hfm = IHomeFolderManager(site)
    principal = factory.object
    master_id = IMasterUser(principal).id
    if not hfm.get(master_id):
        hfm.create(IMasterUser(principal).id)
    homefolder = IHomeFolder(principal)
    if homefolder is None:
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
                prm = IPfincipalRoleManager(homefolder.get(pf))
                if prm.getSetting('uvc.Editor', pid).getName() == 'Unset':
                    prm.assignRoleToPrincipal('uvc.Editor', pid)
                    uvcsite.log('Give uvc.Editor to %s in folder %s' % (pid, pf))
