import grok
import uvcsite.interfaces
import uvcsite.homefolder.homefolder


@grok.subscribe(uvcsite.interfaces.IUVCSite, grok.IObjectAddedEvent)
def homefolder_creation(app, event):
    # We need to do that in an event because of the IIntId registration.
    # If done in the application __init__, the application is not yet
    # persisted, meaning we don't have the DB parenting needed to register
    # our new objects.
    app['members'] = uvcsite.homefolder.homefolder.Members()
