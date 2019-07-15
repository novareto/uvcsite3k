import grok
import uvcsite.auth.handler
import uvcsite.plugins.components
import uvcsite.plugins.subplugins
from uvcsite.plugins.components import Result
from uvcsite.plugins.flags import States, ResultTypes


class UVCAuthenticationPlugin(uvcsite.plugins.subplugins.PAUComponent,
                              uvcsite.plugins.components.Plugin):
    grok.name('uvc.auth')

    title = "UVC authentication"
    description = "Session authentication"
    fa_icon = 'user-lock'

    def __init__(self):
        uvcsite.plugins.components.Plugin.__init__(self)
        uvcsite.plugins.subplugins.PAUComponent.__init__(
            self, uvcsite.auth.handler.UVCAuthenticator,
            'authenticator', local=False)

    @uvcsite.plugins.components.plugin_action(
        'Install', States.NOT_INSTALLED)
    def install(self, site):
        result = uvcsite.plugins.subplugins.PAUComponent.install(self, site)
        return Result(
            value='`Install` was successful.',
            type=ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.components.plugin_action(
        'Uninstall', States.INSTALLED, States.INCONSISTANT)
    def uninstall(self, site):
        result = uvcsite.plugins.subplugins.PAUComponent.uninstall(self, site)
        return Result(
            value='`Uninstall` was successful.',
            type=ResultTypes.MESSAGE,
            redirect=True)
