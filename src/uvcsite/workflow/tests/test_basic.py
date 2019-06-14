import unittest
import uvcsite.content.components
import uvcsite.testing
import uvcsite.workflow


class Person(uvcsite.content.components.Content):
    pass


class TestWorkflowValues(unittest.TestCase):

    def test_values_int(self):
        self.assertEqual(uvcsite.workflow.State.CREATED, 0)
        self.assertEqual(uvcsite.workflow.State.PUBLISHED, 1)
        self.assertEqual(uvcsite.workflow.State.PROGRESS, 2)
        self.assertEqual(uvcsite.workflow.State.REVIEW, 3)

    def test_states_names(self):
        self.assertEqual(
            uvcsite.workflow.State.CREATED.title, "Entwurf")
        self.assertEqual(
            uvcsite.workflow.State.PUBLISHED.title, "gesendet")
        self.assertEqual(
            uvcsite.workflow.State.PROGRESS.title, "in Verarbeitung")
        self.assertEqual(
            uvcsite.workflow.State.REVIEW.title, "Review")


class TestApplicationWorkflow(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        # This is done for each test.
        self.app = self.layer.create_application('app')
        self.klaus = self.app['klaus'] = Person()

    def test_workflow_declaration(self):
        from zope.component import getUtility
        from hurry.workflow.interfaces import IWorkflow
        from hurry.workflow.workflow import Workflow, Transition

        wu = getUtility(IWorkflow)
        self.assertTrue(isinstance(wu, Workflow))

        for name in ('publish', 'create', 'progress', 'review', 'fix'):
            transition = wu.getTransitionById(name)
            self.assertTrue(isinstance(transition, Transition))

        with self.assertRaises(KeyError):
            wu.getTransitionById('noexist')

    def test_initial_content_state(self):
        from hurry.workflow.interfaces import IWorkflowState
        wf = IWorkflowState(self.klaus)
        self.assertEqual(wf.getState(), 0)

    def test_content_publication(self):
        from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo

        #self.assertIsNone(self.klaus.published)
        wf = IWorkflowState(self.klaus)
        IWorkflowInfo(self.klaus).fireTransition('publish')
        self.assertEqual(wf.getState(), 1)
        #self.assertIsNotNone(self.klaus.published)

    def test_content_progress_then_fix(self):
        from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo

        wf = IWorkflowState(self.klaus)
        self.assertEqual(wf.getState(), 0)

        IWorkflowInfo(self.klaus).fireTransition('progress')
        self.assertEqual(wf.getState(), 2)

        IWorkflowInfo(self.klaus).fireTransition('fix')
        self.assertEqual(wf.getState(), 1)
