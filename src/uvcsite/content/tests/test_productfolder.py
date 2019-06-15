import grok
import unittest
import uvcsite.testing
import uvcsite.content.components
import uvcsite.content.directive
from grokcore.component.testing import grok_component
from uvcsite.tests import fixtures


class TestProductFolder(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        grok_component('AddressBook', fixtures.addressbook.AddressBook)

    def test_container_declaration(self):
        addressbook = fixtures.addressbook.AddressBook()
        self.assertEqual(addressbook.name, 'addressbook')
        self.assertEqual(addressbook.title, 'Adressbuch')
        self.assertEqual(addressbook.description, 'Adressbuch ...')
        self.assertIs(addressbook.getContentType(),
                      fixtures.addressbook.Contact)

    def test_productfolder_utility(self):
        from zope.component import getUtilitiesFor
        from uvcsite.content.interfaces import IProductFolder

        products = list(getUtilitiesFor(IProductFolder))
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][0], 'Addressbook')
