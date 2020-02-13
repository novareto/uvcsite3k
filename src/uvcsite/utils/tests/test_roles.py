# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import uvcsite
import unittest


from uvcsite.interfaces import IMyRoles
from uvcsite.content.principal import Principal
from zope.security.interfaces import IPrincipal


class TestRolesMethods(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        # This is done for each test.
        self.app = self.layer.create_application('app')
        utility = uvcsite.interfaces.IHomeFolderManager(self.app)
        homefolder = utility.create('0101010001')

    def test_checkRoles(self):
        principal = Principal('0101010001', '0101010001')
        self.assertTrue(IPrincipal(principal))
        roles = IMyRoles(principal)
        self.assertEqual(roles.getAllRoles(), ['ENMS'])

