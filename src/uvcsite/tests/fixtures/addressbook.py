import grok
import zope.schema
import zope.interface
import zope.component
import zope.security

import uvcsite.content.components
import uvcsite.content.directive
import uvcsite.content.interfaces


class IContact(uvcsite.content.interfaces.IContent):

    name = zope.schema.TextLine(
        title=u"Name",
        description="Some name")

    alter = zope.schema.Int(
        title=u"Alter",
        description=u"Wie ist ihr Alter",
        required=False)


class IAddressBook(uvcsite.content.interfaces.IProductFolder):
    """Marker Interface
    """


@uvcsite.content.directive.schema(IContact)
class Contact(uvcsite.content.components.Content):
    grok.name(u'Kontakt')


@zope.interface.implementer(IAddressBook)
class AddressBook(uvcsite.content.components.ProductFolder):
    grok.name('addressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.content.directive.contenttype(Contact)



