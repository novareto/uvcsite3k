import grok
import uvcsite.permissions
from zope.interface import Interface


class MinimalAppIndex(grok.View):
    grok.name("index")
    grok.context(Interface)
    grok.require('zope.View')

    def render(self):
        return "Hallo Welt"
