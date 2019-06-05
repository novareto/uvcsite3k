import unittest
import uvcsite.tests
import uvcsite.app

from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer


class MyTestCase(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)



browser_layer = ZopeFanstaticBrowserLayer(uvcsite.tests)

class MyFunctionalTestCase(unittest.TestCase):

    layer = browser_layer

    def setUp(self):
        self.app = uvcsite.app.Uvcsite()
    
    def test_foo(self):
        index = queryMultiAdapter((self.app, TestRequest()), name='index')
        self.assertNotEqual(index, None)

        # There is no view called 'index2'
        index2 = queryMultiAdapter((self.app, TestRequest()), name='index2')
        self.assertEqual(index2, None)
