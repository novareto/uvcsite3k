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
