import grok
import zope.interface
import zope.authentication.interfaces 
import zope.pluggableauth

import uvcsite.interfaces
import uvcsite.plugins


def setup_pau(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = ("cookies",
                              "Zope Realm Basic-Auth",
                              "No Challenge if Authenticated",)


@zope.interface.implementer(uvcsite.interfaces.IUVCSite) 
class Uvcsite(grok.Application, grok.Container):
    grok.traversable('plugins')

    grok.local_utility(
        zope.pluggableauth.PluggableAuthentication,
        zope.authentication.interfaces.IAuthentication,
        public=True,
        setup=setup_pau)

    @property
    def plugins(self):
        return uvcsite.plugins.PluginsPanel('plugins', self)
