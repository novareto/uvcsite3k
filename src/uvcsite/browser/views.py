import grok
import uvcsite.browser
import uvcsite.app
import uvcsite.resource

from uvcsite.interfaces import IUVCSite



class Index(grok.View):
    grok.context(IUVCSite)

    def render(self):
        return u"Hallo Welt"
