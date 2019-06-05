import grok
import zope.interface

import uvcsite.interfaces
import uvcsite.plugins


@zope.interface.implementer(uvcsite.interfaces.IUVCSite) 
class Uvcsite(grok.Application, grok.Container):
    grok.traversable('plugins')

    @property
    def plugins(self):
        return uvcsite.plugins.PluginsPanel('plugins', self)
