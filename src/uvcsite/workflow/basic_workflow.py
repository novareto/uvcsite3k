import enum
import grok
import hurry.workflow.workflow
import hurry.workflow.interfaces


class Workflow(hurry.workflow.workflow.Workflow):

    STATES_NAMES = {
        0: 'Entwurf',
        1: 'gesendet',
        2: 'in Verarbeitung',
        3: 'Review'
    }

    class State(enum.IntEnum):
        CREATED = 0
        PUBLISHED = 1
        PROGRESS = 2
        REVIEW = 3

        @property
        def title(self):
            return STATES_NAMES[self.value]

    @classmethod
    def create(cls):
        return cls([
            hurry.workflow.workflow.Transition(
                transition_id='create',
                title='create',
                source=None,
                destination=cls.State.CREATED),

            hurry.workflow.workflow.Transition(
                transition_id='publish',
                title='publish',
                source=cls.State.CREATED,
                destination=cls.State.PUBLISHED),
            
            hurry.workflow.workflow.Transition(
                transition_id='progress',
                title='progress',
                source=cls.State.CREATED,
                destination=cls.State.PROGRESS),
            
            hurry.workflow.workflow.Transition(
                transition_id='fix',
                title='fix',
                source=cls.State.PROGRESS,
                destination=cls.State.PUBLISHED),
            
            hurry.workflow.workflow.Transition(
                transition_id='review',
                title='publish_to_review',
                source=cls.State.CREATED,
                destination=cls.State.REVIEW),
            
            hurry.workflow.workflow.Transition(
                transition_id='review_to_publish',
                title='review to publish',
                source=cls.State.REVIEW,
                destination=cls.State.PUBLISHED)])


grok.global_utility(
    Workflow.create(),
    provides=hurry.workflow.interfaces.IWorkflow,
    direct=True)
