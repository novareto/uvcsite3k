import grok
import hurry.workflow.interfaces
import zope.security.interfaces

from zope.securitypolicy.interfaces import (
    IPrincipalPermissionManager, IRolePermissionManager)

import uvcsite.auth.interfaces
import uvcsite.permissions
from uvcsite.workflow.workflow import Workflow


def named(component):
    return grok.name.bind().get(component)


@grok.subscribe(hurry.workflow.interfaces.IWorkflowTransitionEvent)
def remove_edit_permission(event):
    if event.destination == Workflow.states.PUBLISHED:
        IRolePermissionManager(event.object).denyPermissionToRole(
            named(uvcsite.permissions.Edit), named(uvcsite.permissions.Editor))


@grok.subscribe(hurry.workflow.interfaces.IWorkflowTransitionEvent)
def change_permissions(event):
    if event.destination == Workflow.states.PUBLISHED:
        try:
            principal = uvcsite.utils.shorties.getPrincipal()
        except zope.security.interfaces.NoInteraction:
            return
        else:
            if not uvcsite.auth.interfaces.ICOUser.providedBy(principal):
                return

        prinper = IPrincipalPermissionManager(event.object)
        roleper = IRolePermissionManager(event.object)
        roleper.denyPermissionToRole(
            named(uvcsite.permissions.View), named(uvcsite.permissions.Editor))
        prinper.grantPermissionToPrincipal(
            named(uvcsite.permissions.View), event.object.principal.id)
