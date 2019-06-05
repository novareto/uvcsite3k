import grok
import uvcsite.browser
import uvcsite.app
import uvcsite.resource


class Index(uvcsite.browser.Page):
    grok.context(uvcsite.app.Uvcsite)
    
    def update(self):
        uvcsite.resource.style.need()

    def render(self):
        return "I'm uvcsite."
