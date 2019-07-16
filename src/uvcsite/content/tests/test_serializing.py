import unittest
import uvcsite.content.interfaces
import uvcsite.testing
from uvcsite.tests import fixtures
from zope.component import getAdapter


class TestSerialization(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        self.content = fixtures.addressbook.Contact()
    
    def test_json_adapter(self):
        serializer = getAdapter(
            self.content,
            uvcsite.content.interfaces.ISerializer,
            name="application/json")
        with self.assertRaises(NotImplementedError):
            serializer()
        
    def test_xml_adapter(self):
        serializer = getAdapter(
            self.content,
            uvcsite.content.interfaces.ISerializer,
            name="application/xml")
        with self.assertRaises(NotImplementedError):
            serializer()
