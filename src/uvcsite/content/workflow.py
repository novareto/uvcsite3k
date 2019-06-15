import grok
import uvcsite.content.interfaces
import hurry.workflow.workflow
import hurry.workflow.interfaces


class WorkflowState(hurry.workflow.workflow.WorkflowState, grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.provides(hurry.workflow.interfaces.IWorkflowState)


class WorkflowInfo(hurry.workflow.workflow.WorkflowInfo, grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)
    grok.provides(hurry.workflow.interfaces.IWorkflowInfo)


@grok.subscribe(uvcsite.content.interfaces.IContent, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
    hurry.workflow.interfaces.IWorkflowInfo(content).fireTransition('create')
