# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import unittest

from uvcsite import testing
from uvcsite.content import principal
from grokcore.component.testing import grok
from zope.security.interfaces import IPrincipal
from uvcsite.auth.event import applyPermissionsForExistentCoUsers


class TestPrincipal(unittest.TestCase):
    layer = testing.application_layer

    def setUp(self):
        grok("uvcsite.tests.fixtures.usermanagement")

    def test_principal(self):
        pr = principal.Principal("0101010001")
        self.assertTrue(isinstance(pr, principal.Principal))
        self.assertTrue(IPrincipal.providedBy(pr))

        class F:
            def __init__(self, pr):
                self.object = pr

        with testing.AuthenticatedRequest("0101010001"):
            self.layer.create_application("app")
            applyPermissionsForExistentCoUsers(F(pr))
            self.assertEqual(str(pr.homefolder), "<Homefolder for 0101010001>")
            self.assertEqual(
                pr.homefolder_url, "http://127.0.0.1/app/members/0101010001"
            )
