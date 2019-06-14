import unittest
import uvcsite.content.components
import uvcsite.interfaces
import uvcsite.testing
import uvcsite.homefolder.homefolder


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
