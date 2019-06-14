import grok
import uvcsite.content.interfaces
import hurry.workflow.workflow
import hurry.workflow.interfaces


class State:

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return hurry.workflow.interfaces.IWorkflowState(instance).getState()

    def __set__(self, instance, state):
        hurry.workflow.interfaces.IWorkflowInfo(instance).fireTransitionToward(
            state)

    def __delete__(self, instance):
        raise NotImplementedError('Implement me if need be.')


### This should go to /content
class WorkflowState(hurry.workflow.workflow.WorkflowState, grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.provides(hurry.workflow.interfaces.IWorkflowState)


class WorkflowInfo(hurry.workflow.workflow.WorkflowInfo, grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.provides(hurry.workflow.interfaces.IWorkflowInfo)


@grok.subscribe(uvcsite.content.interfaces.IContent, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
     hurry.workflow.interfaces.IWorkflowInfo(content).fireTransition('create')


### This should go to /auth
#@grok.subscribe(hurry.workflow.interfaces.IWorkflowTransitionEvent)
def change_permissions(event):
    if event.destination == PUBLISHED:
        obj = event.object
        principal = obj.principal
        from uvcsite.auth.interfaces import ICOUser
        from zope.securitypolicy import interfaces
        if not ICOUser.providedBy(uvcsite.getPrincipal()):
            prinper = interfaces.IPrincipalPermissionManager(obj)
            roleper = interfaces.IRolePermissionManager(obj)
            roleper.denyPermissionToRole('uvc.ViewContent', 'uvc.Editor')
            prinper.grantPermissionToPrincipal('uvc.ViewContent', principal.id)
