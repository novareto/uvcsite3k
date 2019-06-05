import grok
from uvcsite import resource


class Uvc3k(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self):
        resource.style.need()
