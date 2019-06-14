import unittest
import uvcsite.content.components
import uvcsite.testing
import uvcsite.workflow
from uvcsite.workflow.workflow import Workflow


class Person(uvcsite.content.components.Content):
    pass


class TestWorkflowValues(unittest.TestCase):

    def test_values_int(self):
        self.assertEqual(Workflow.states.CREATED, 0)
        self.assertEqual(Workflow.states.PUBLISHED, 1)
        self.assertEqual(Workflow.states.PROGRESS, 2)
        self.assertEqual(Workflow.states.REVIEW, 3)

    def test_states_names(self):
        self.assertEqual(Workflow.states.CREATED.title, "Entwurf")
        self.assertEqual(Workflow.states.PUBLISHED.title, "gesendet")
        self.assertEqual(Workflow.states.PROGRESS.title, "in Verarbeitung")
        self.assertEqual(Workflow.states.REVIEW.title, "Review")


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
        self.assertEqual(self.klaus.state, 0)

    def test_content_publication(self):
        self.klaus.state = Workflow.states.PUBLISHED

        self.assertEqual(self.klaus.state, 1)

    def test_invalid_transition(self):
        from hurry.workflow.interfaces import NoTransitionAvailableError

        self.klaus.state = Workflow.states.PUBLISHED
        with self.assertRaises(NoTransitionAvailableError):
            self.klaus.state = Workflow.states.PROGRESS

    def test_content_progress_then_publish(self):        
        self.klaus.state = Workflow.states.PROGRESS
        self.klaus.state = Workflow.states.PUBLISHED


class TestApplicationWorkflowXMLRPC(unittest.TestCase):
    layer = uvcsite.testing.xmlrpc_layer

    def setUp(self):
        # This is done for each test.
        self.app = self.layer.create_application('app')
        self.klaus = self.app['klaus'] = Person()

    def test_workflow_xmlrpc_faulty_transition(self):
        from xmlrpc.client import ProtocolError

        server = self.layer.xmlrpc_server(
            "http://localhost/app/", handle_errors=True)

        self.assertIsNone(server.klaus.publish())
        self.assertEqual(server.klaus.state(), Workflow.states.PUBLISHED)
        with self.assertRaises(ProtocolError):
            server.klaus.publish()

    def test_workflow_xmlrpc_progress_fix(self):
        server = self.layer.xmlrpc_server(
            "http://localhost/app/", handle_errors=True)

        self.assertEqual(server.klaus.state(), Workflow.states.CREATED)
        self.assertIsNone(server.klaus.progress())
        self.assertIsNone(server.klaus.fix())
        self.assertEqual(server.klaus.state(), Workflow.states.PUBLISHED)

    def test_workflow_xmlrpc_review_publish(self):
        from xmlrpc.client import ProtocolError

        server = self.layer.xmlrpc_server(
            "http://localhost/app/", handle_errors=True)

        self.assertIsNone(server.klaus.review())
        self.assertEqual(server.klaus.state(), Workflow.states.REVIEW)
        self.assertIsNone(server.klaus.publish())
        self.assertEqual(server.klaus.state(), Workflow.states.PUBLISHED)
