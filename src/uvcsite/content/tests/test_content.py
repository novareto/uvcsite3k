import grok
import unittest
import uvcsite.testing
import uvcsite.content.components
import uvcsite.content.directive
import zope.schema
import zope.schema.interfaces
from uvcsite.tests import fixtures


class TestContentComponent(unittest.TestCase):

    def test_base_content(self):
        content = uvcsite.content.components.Content()
        self.assertEqual(content.meta_type, "Content")
        self.assertEqual(content.schema, tuple())

    def test_content_with_schema_no_values(self):
        content = fixtures.addressbook.Contact()
        self.assertEqual(content.meta_type, "Contact")
        self.assertEqual(content.schema, (fixtures.addressbook.IContact,))

    def test_content_with_schema_and_values(self):
        content = fixtures.addressbook.Contact(name="Magnus", alter=45)
        self.assertEqual(content.name, "Magnus")
        self.assertEqual(content.alter, 45)

        with self.assertRaises(zope.schema.interfaces.WrongType):
            content = fixtures.addressbook.Contact(name="Magnus", alter="42")

        with self.assertRaises(AttributeError):
            content = fixtures.Contact(error=12)


class TestContentLifecycle(unittest.TestCase):
    layer = uvcsite.testing.application_layer
    
    def test_content_creation_modification(self):
        import datetime
        import zope.security
        from zope.publisher.browser import TestRequest
        from zope.pluggableauth.factories import Principal
        from zope.lifecycleevent import ObjectCreatedEvent

        with uvcsite.testing.AuthenticatedRequest('0101010001') as request:
            content = uvcsite.content.components.Content()
            self.assertEqual(content.principal, request.principal)

        grok.notify(ObjectCreatedEvent(content))
        self.assertTrue(content.modtime, datetime.datetime)
