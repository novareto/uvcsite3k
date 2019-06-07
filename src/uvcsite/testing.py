import transaction
import unittest
import uvcsite.tests
import uvcsite.app

from zope.component import provideUtility
from zope.component.hooks import setSite
from zope.publisher.browser import TestRequest
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer


class UVCSiteLayer(ZopeFanstaticBrowserLayer):

    def testSetUp(self):
        super().testSetUp()
        root = self.getRootFolder()
        with transaction.manager:
            app = root["app"] = uvcsite.app.Uvcsite()
        setSite(app)

    def testTearDown(self):
        root = self.getRootFolder()
        with transaction.manager:
           del root["app"]
        setSite()
        super().testTearDown()


browser_layer = UVCSiteLayer(uvcsite.tests)
