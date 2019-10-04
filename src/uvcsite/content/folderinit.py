import grok
import uvcsite.interfaces
import uvcsite.content.productregistration
from zope.pluggableauth.factories import Principal


@grok.subscribe(uvcsite.interfaces.IHomeFolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    import pdb; pdb.set_trace()
    for sub in uvcsite.content.productregistration.get_product_registrations(
            principal, discard_unavailable=True):
        sub.create(container=homefolder)
