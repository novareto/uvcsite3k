import grok
from uvcsite.content.events import AfterSaveEvent
import uvcsite.browser
import zeam.form.base
import zope.lifecycleevent

from zeam.form.base.markers import NO_VALUE, NO_CHANGE
from zeam.form.base.interfaces import IDataManager
from zeam.form.base.datamanager import ObjectDataManager
from zope.event import notify
from zope.lifecycleevent import Attributes, ObjectModifiedEvent


def set_fields_data(fields, content, data):
    """Applies the values to the fields, if a change has been made and
    if the field is present in the given fields manager. It returns a
    dictionnary describing the changes applied with the name of the field
    and the interface from where it's from.
    """
    changes = {}
    if not IDataManager.providedBy(content):
        content = ObjectDataManager(content)

    for identifier, value in data.items():
        field = fields.get(identifier, default=None)
        if field is None or value is NO_VALUE or value is NO_CHANGE:
            continue

        content.set(identifier, value)
        changes.setdefault(field.interface, []).append(identifier)

    return changes


def notify_changes(content, changes, event=ObjectModifiedEvent):
    """Builds a list of descriptions, made of Attributes objects, defining
    the changes made on the content and the related interface.
    """
    assert event is not None

    if changes:
        descriptions = []
        for interface, names in changes.items():
            descriptions.append(Attributes(interface, *names))
        notify(event(content, *descriptions))
        return descriptions
    return None


def apply_data_event(fields, content, data, event=ObjectModifiedEvent):
    """ Updates the object with the data and sends an IObjectModifiedEvent
    """
    changes = set_fields_data(fields, content, data)
    if changes:
        if IDataManager.providedBy(content):
            notify_changes(content.content, changes, event)
        else:
            notify_changes(content, changes, event)
    return changes


class AddForm(uvcsite.browser.Form):
    grok.baseclass()
    grok.require('uvc.AddContent')

    _finishedAdd = False

    @zeam.form.base.action(u'Speichern', identifier="uvcsite.add")
    def handleAdd(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten')
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            grok.notify(AfterSaveEvent(obj, self.request))

    def createAndAdd(self, data):
        obj = self.create(data)
        grok.notify(zope.lifecycleevent.ObjectCreatedEvent(obj))
        self.add(obj)
        return obj

    def create(self, data):
        raise NotImplementedError

    def add(self, object):
        raise NotImplementedError

    def nextURL(self):
        raise NotImplementedError

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super().render()
