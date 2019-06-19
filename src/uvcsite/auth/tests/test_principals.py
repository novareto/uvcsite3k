import unittest
import uvcsite.content.components
import uvcsite.interfaces
import uvcsite.testing
from zope.pluggableauth.factories import Principal
from zope.security.interfaces import IPrincipal
from uvcsite.auth.interfaces import IMasterUser
from grokcore.component.testing import grok


class TestMasterUser(unittest.TestCase):
    layer = uvcsite.testing.application_layer
    
    def test_master_user(self):
        principal = Principal('0101010001')
        self.assertTrue(IPrincipal.providedBy(principal))

        masteruser = IMasterUser(principal)
        self.assertTrue(masteruser is principal)
        self.assertTrue(IPrincipal.providedBy(masteruser))
        self.assertEqual(masteruser.id, "0101010001")

    def test_co_user(self):
        principal = Principal('0101010001-01')
        self.assertTrue(IPrincipal.providedBy(principal))

        co_user = IMasterUser(principal)
        self.assertFalse(co_user is principal)
        self.assertEqual(co_user.id, "0101010001")


class TestGroup(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        grok('uvcsite.tests.fixtures.usermanagement')
    
    def test_principal_groups(self):
        app = self.layer.create_application('app')
        with uvcsite.testing.Request('0101010001') as request:
            self.assertEqual(request.principal.id, '0101010001')
            self.assertEqual(
                request.principal.groups,
                ['zope.Everybody', 'zope.Authenticated', 'uvc.Member'])
