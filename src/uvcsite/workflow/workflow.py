import enum
import grok
import hurry.workflow.workflow
import hurry.workflow.interfaces


class State(enum.IntEnum):
        CREATED = 0
        PUBLISHED = 1
        PROGRESS = 2
        REVIEW = 3

        @property
        def title(self):
            return STATES_NAMES[self.value]


STATES_NAMES = {
    State.CREATED: 'Entwurf',
    State.PUBLISHED: 'gesendet',
    State.PROGRESS: 'in Verarbeitung',
    State.REVIEW: 'Review'
}


class Workflow(hurry.workflow.workflow.Workflow):

    states = State

    @classmethod
    def create(cls):
        return cls([
            hurry.workflow.workflow.Transition(
                transition_id='create',
                title='create',
                source=None,
                destination=cls.states.CREATED),

            hurry.workflow.workflow.Transition(
                transition_id='publish',
                title='publish',
                source=cls.states.CREATED,
                destination=cls.states.PUBLISHED),

            hurry.workflow.workflow.Transition(
                transition_id='progress',
                title='progress',
                source=cls.states.CREATED,
                destination=cls.states.PROGRESS),

            hurry.workflow.workflow.Transition(
                transition_id='fix',
                title='fix',
                source=cls.states.PROGRESS,
                destination=cls.states.PUBLISHED),

            hurry.workflow.workflow.Transition(
                transition_id='review',
                title='publish_to_review',
                source=cls.states.CREATED,
                destination=cls.states.REVIEW),

            hurry.workflow.workflow.Transition(
                transition_id='review_to_publish',
                title='review to publish',
                source=cls.states.REVIEW,
                destination=cls.states.PUBLISHED)])


grok.global_utility(
    Workflow.create(),
    provides=hurry.workflow.interfaces.IWorkflow,
    direct=True)
