import unittest
import uvcsite.content.components
import uvcsite.interfaces
import uvcsite.testing
import uvcsite.homefolder.homefolder
import zope.securitypolicy.settings

from uvcsite.tests import fixtures


class TestAPI(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        self.app = self.layer.create_application('app')
        self.app['addressbook'] = fixtures.addressbook.AddressBook()
        
    def test_json_api(self):
        self.assertTrue('addressbook' in self.app)
