import unittest

from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest

from zope.fanstatic.testing import ZopeFanstaticBrowserLayer

import uvc3k.tests
from uvc3k.app import Uvc3k

# In this file we create a unittest, a functional unittest.

class MyTestCase(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)

browser_layer = ZopeFanstaticBrowserLayer(uvc3k.tests)

class MyFunctionalTestCase(unittest.TestCase):

    layer = browser_layer

    def test_foo(self):
        index = queryMultiAdapter((Uvc3k(), TestRequest()), name='index')
        self.assertNotEqual(index, None)

        # There is no view called 'index2'
        index2 = queryMultiAdapter((Uvc3k(), TestRequest()), name='index2')
        self.assertEqual(index2, None)

