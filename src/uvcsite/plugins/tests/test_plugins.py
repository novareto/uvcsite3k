import unittest
import zope.interface.verify
import uvcsite.interfaces
import uvcsite.testing
import uvcsite.plugins.flags
import uvcsite.plugins.components


class TestPluginsComponents(unittest.TestCase):

    def test_status(self):
        """Idempotency test
        """
        status = uvcsite.plugins.components.Status(
            uvcsite.plugins.flags.States.NOT_INSTALLED, 'Some info')
        self.assertEqual(
            uvcsite.plugins.flags.States.NOT_INSTALLED, status.state)

        status = uvcsite.plugins.components.Status(
            'not installed', 'Some info')
        self.assertEqual(
            uvcsite.plugins.flags.States.NOT_INSTALLED, status.state)

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            status = uvcsite.plugins.components.Status(
                'wrong', 'Some info')

    def test_status_representation(self):
        status = uvcsite.plugins.components.Status(
            uvcsite.plugins.flags.States.INSTALLED, 'Some info')
        self.assertEqual('installed', str(status))
        self.assertEqual('<Status "installed">', repr(status))

    def test_result(self):
        """Idempotency test
        """
        result = uvcsite.plugins.components.Result(
            uvcsite.plugins.flags.ResultTypes.JSON, '"Some info"')
        self.assertEqual(
            uvcsite.plugins.flags.ResultTypes.JSON, result.type)

        result = uvcsite.plugins.components.Result(
            'application/json', '"Some info"')
        self.assertEqual(
            uvcsite.plugins.flags.ResultTypes.JSON, result.type)

    def test_result_representation(self):
        result = uvcsite.plugins.components.Result(
            uvcsite.plugins.flags.ResultTypes.JSON, '"Some info"')
        self.assertEqual('application/json', str(result))
        self.assertEqual(
            '<Result "application/json" redirect=False>', repr(result))
        
        result = uvcsite.plugins.components.Result(
            uvcsite.plugins.flags.ResultTypes.JSON, '"Some info"', True)
        self.assertEqual(
            '<Result "application/json" redirect=True>', repr(result))


class TestPlugins(unittest.TestCase):
    layer = uvcsite.testing.application_layer

    def setUp(self):
        self.app = self.layer.create_application('app')

    def test_simple_plugin(self):
        plugin = uvcsite.plugins.components.Plugin()
        self.assertEqual(None, plugin.title)
        self.assertEqual("", plugin.description)
        self.assertEqual(uvcsite.plugins.components.Status(
            state=uvcsite.plugins.flags.States.NOT_INSTALLED), plugin.status)
        self.assertEqual(None, plugin.actions)
        self.assertTrue(zope.interface.verify.verifyObject(
            uvcsite.plugins.components.IPlugin, plugin))
