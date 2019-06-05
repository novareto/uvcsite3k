import grok
import uvcsite.content.interfaces
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState


class WorkflowAPI(grok.XMLRPC):
    grok.context(uvcsite.content.interfaces.IContent)

    def publish(self):
        return IWorkflowInfo(self.context).fireTransition('publish')

    def progress(self):
        return IWorkflowInfo(self.context).fireTransition('progress')

    def fix(self):
        return IWorkflowInfo(self.context).fireTransition('fix')

    def state(self):
        return IWorkflowState(self.context).getState()
