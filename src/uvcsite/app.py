import grok
import uvcsite.interfaces
import zope.interface


@zope.interface.implementer(uvcsite.interfaces.IUVCSite) 
class Uvcsite(grok.Application, grok.Container):
    pass
