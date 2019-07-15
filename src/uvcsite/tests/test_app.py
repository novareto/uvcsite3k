import unittest
import uvcsite.interfaces
import uvcsite.testing


class TestAPI(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        self.app = self.layer.create_application('app')

    def test_nothing_yet(self):
        self.assertTrue(True)
