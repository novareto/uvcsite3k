import grok
import uvcsite.permissions
from zope.interface import Interface


class IndexPage(grok.View):
    grok.name("index")
    grok.baseclass()
    grok.context(Interface)
    grok.require(uvcsite.permissions.View)

    def render(self):
        return "Hallo Welt"
