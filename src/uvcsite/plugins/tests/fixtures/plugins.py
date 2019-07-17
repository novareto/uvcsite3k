import grok
import uvcsite.plugins


class MockPlugin(uvcsite.plugins.components.Plugin):
    grok.name('mockup')

    description = "Mockup plugin"

    @uvcsite.plugins.components.plugin_action(
        'Text', uvcsite.plugins.flags.States.NOT_INSTALLED)
    def some_text(self, site):
        return uvcsite.plugins.components.Result(
            value="Magnificent text.",
            type=uvcsite.plugins.flags.ResultTypes.PLAIN)

    @uvcsite.plugins.components.plugin_action(
        'JSON', uvcsite.plugins.flags.States.INSTALLED)
    def a_bit_of_json(self, site):
        return uvcsite.plugins.components.Result(
            value="{1: ['a', 'b'}",
            type=uvcsite.plugins.flags.ResultTypes.JSON)
