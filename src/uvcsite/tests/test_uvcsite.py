import unittest
import uvcsite.tests
import uvcsite.app
from zope.component import provideUtility

from zope.component import queryMultiAdapter
from zope.component.hooks import setSite
from zope.publisher.browser import TestRequest
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer


class MyTestCase(unittest.TestCase):
    def test_foo(self):
        self.assertEqual(1, 1)


class UVCSiteLayer(ZopeFanstaticBrowserLayer):
    def setUp(self):
        super(UVCSiteLayer, self).setUp()
        root = self.getRootFolder()
        from uvcsite.app import Uvcsite
        from uvcsite.tests.fixtures.usermanagement import UserManagement
        from uvcsite.extranetmembership.interfaces import IUserManagement

        root["app"] = Uvcsite()
        setSite(root['app'])
        provideUtility(UserManagement(), IUserManagement)
        import transaction

        transaction.commit()


browser_layer = UVCSiteLayer(uvcsite.tests)


class MyFunctionalTestCase(unittest.TestCase):

    layer = browser_layer

    def setUp(self):
        self.app = uvcsite.app.Uvcsite()

    def test_foo(self):
        index = queryMultiAdapter((self.app, TestRequest()), name="index")
        self.assertNotEqual(index, None)

        # There is no view called 'index2'
        index2 = queryMultiAdapter((self.app, TestRequest()), name="index2")
        self.assertEqual(index2, None)
