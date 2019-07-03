import unittest
import uvcsite.content.components
import uvcsite.interfaces
import uvcsite.testing
import uvcsite.homefolder.homefolder
import zope.securitypolicy.settings


class TestHomefolder(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        # This is done for each test.
        self.app = self.layer.create_application('app')

    def test_app_has_members_container(self):
        import zope.component

        self.assertTrue('members' in self.app)
        self.assertTrue(isinstance(
            self.app['members'], uvcsite.homefolder.homefolder.Members))

    def test_homefolder_manager_existance(self):
        utility = uvcsite.interfaces.IHomeFolderManager(self.app)
        self.assertTrue(isinstance(
            utility, uvcsite.homefolder.homefolder.PortalMembership))

        self.assertTrue(utility.container is self.app['members'])

    def test_homefolder_manager_getters(self):
        utility = uvcsite.interfaces.IHomeFolderManager(self.app)
        with self.assertRaises(KeyError):
            utility['lars']

        self.assertIsNone(utility.get('lars'))

        homefolder = utility.create('lars')
        self.assertTrue(utility['lars'] is homefolder)
        self.assertTrue(utility.get('lars') is homefolder)

    def test_homefolder_creation_roles(self):
        from zope.securitypolicy.interfaces import IPrincipalRoleManager
        
        utility = uvcsite.interfaces.IHomeFolderManager(self.app)
        homefolder = utility.create('lars')

        prm = IPrincipalRoleManager(homefolder)
        for role, setting in prm.getRolesForPrincipal('lars'):
            self.assertTrue(role in utility.owner_roles)
            self.assertEqual(setting, zope.securitypolicy.settings.Allow)

    def test_unexisting_homefolder_resolution(self):
        with uvcsite.testing.AuthenticatedRequest('lars') as request:
            self.assertIsNone(uvcsite.interfaces.IHomeFolder(request.principal, None))

    def test_homefolder_resolution(self):
        utility = uvcsite.interfaces.IHomeFolderManager(self.app)
        homefolder = utility.create('lars')
        with uvcsite.testing.AuthenticatedRequest('lars') as request:
            found = uvcsite.interfaces.IHomeFolder(request.principal)
            self.assertTrue(found is homefolder)
