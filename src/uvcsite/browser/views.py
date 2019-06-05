import grok
import uvcsite.app
import uvcsite.resource


class Index(grok.View):
    grok.context(uvcsite.app.Uvcsite)
    
    def update(self):
        uvcsite.resource.style.need()

    def render(self):
        return "I'm uvcsite."
