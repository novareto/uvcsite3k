import grok
import uvcsite.interfaces
import uvcsite.content.productregistration

from zope.pluggableauth.factories import Principal
from uvcsite.auth.event import IUserLoggedInEvent


@grok.subscribe(uvcsite.interfaces.IHomeFolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    for sub in uvcsite.content.productregistration.get_product_registrations(
            principal, discard_unavailable=True):
        sub.create(container=homefolder)


@grok.subscribe(IUserLoggedInEvent)
def add_product_folders(factory):
    principal = factory.object
    for sub in uvcsite.content.productregistration.get_product_registrations(
            principal, discard_unavailable=True):
        sub.create(container=homefolder)
