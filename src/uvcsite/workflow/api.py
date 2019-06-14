import grok
import uvcsite.content.interfaces
from uvcsite.workflow.workflow import Workflow


class WorkflowAPI(grok.XMLRPC):
    grok.context(uvcsite.content.interfaces.IContent)

    def publish(self):
        self.context.state = Workflow.states.PUBLISHED

    def review(self):
        self.context.state = Workflow.states.REVIEW
        
    def progress(self):
        self.context.state = Workflow.states.PROGRESS

    def fix(self):
        self.context.state = Workflow.states.PUBLISHED

    def state(self):
        return self.context.state.value
