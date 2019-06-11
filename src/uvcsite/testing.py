import transaction
import unittest
import uvcsite.tests
import uvcsite.app
import grokcore.site.util

from zope.component import provideUtility
from zope.component.hooks import setSite
from zope.publisher.browser import TestRequest
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer


class UVCSiteLayer(ZopeFanstaticBrowserLayer):

    def create_application(self, name):
        root = self.getRootFolder()
        if name in root:
            raise KeyError('Application already exists.')
        with transaction.manager:
            grokcore.site.util.create_application(
                uvcsite.app.Uvcsite, root, name)
        app = root[name]
        setSite(app)
        return app

    def testTearDown(self):
        super().testTearDown()
        setSite()


browser_layer = UVCSiteLayer(uvcsite.tests)
