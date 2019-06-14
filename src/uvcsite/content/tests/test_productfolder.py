import grok
import unittest
import uvcsite.testing
import uvcsite.content.components
import uvcsite.content.directive
from grokcore.component.testing import grok_component


class Contact(uvcsite.content.components.Content):
    pass


class AdressBook(uvcsite.content.components.ProductFolder):
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.content.directive.contenttype(Contact)


class TestProductFolder(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        grok_component('AdressBook', AdressBook)

    def test_productfolder_utility(self):
        from zope.component import getUtilitiesFor
        from uvcsite.content.interfaces import IProductFolder

        products = list(getUtilitiesFor(IProductFolder))
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][0], 'Adressbook')
