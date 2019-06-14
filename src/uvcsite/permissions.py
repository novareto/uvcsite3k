import grok
from uvcsite.workflow.basic_workflow import Workflow
from zope.securitypolicy.interfaces import IRolePermissionManager
from hurry.workflow.interfaces import IWorkflowTransitionEvent


class View(grok.Permission):
    grok.name('uvc.ViewContent')


class Add(grok.Permission):
    grok.name('uvc.AddContent')


class Edit(grok.Permission):
    grok.name('uvc.EditContent')


class User(grok.Role):
    grok.name('uvc.User')
    grok.permissions(
        'zope.View'
    )


class AccessHomeFolder(grok.Permission):
    grok.name('uvc.AccessHomeFolder')


class HomeFolderUser(grok.Role):
    grok.name('uvc.HomeFolderUser')
    grok.permissions(
        AccessHomeFolder
    )


class Editor(grok.Role):
    grok.name('uvc.Editor')
    grok.permissions(
        View,
        Add,
        Edit,
        AccessHomeFolder)


def named(component):
    return grok.name.bind().get(component)

    
@grok.subscribe(IWorkflowTransitionEvent)
def remove_edit_permission(event):
    if event.destination != Workflow.State.PUBLISHED:
        return
    IRolePermissionManager(event.object).denyPermissionToRole(
           named(Edit), named(Editor))
