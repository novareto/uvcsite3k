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
