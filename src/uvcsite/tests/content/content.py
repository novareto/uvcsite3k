"""
Content
=======

:doctest:
:layer: uvcsite.tests.browser_layer


BaseClasses
-----------

  >>> from uvcsite.content.components import Content, ProductFolder

  >>> content = Content()
  >>> content.schema
  ()

  >>> print(content.meta_type)
  Content

Setup
-----
First start with makeing an instance of the Content 

  >>> contact = Contact() 
  >>> contact 
  <uvcsite.tests.content.content.Contact object at ...> 

Attributes
----------
There should be the two attributes from our IContent Schema

  >>> contact.name

  >>> contact.alter


Schema
------

  >>> contact.schema
  (<InterfaceClass uvcsite.tests.content.content.IContact>,)

"""

import grok
import zope.schema
import uvcsite.content.directive
import uvcsite.content.components
import uvcsite.content.interfaces


class IContact(uvcsite.content.interfaces.IContent):

    name = zope.schema.TextLine(
        title=u"Name",
        description="Some name",
    )

    alter = zope.schema.TextLine(
        title=u"Alter",
        description=u"Wie ist ihr Alter",
        required=False
    )


@uvcsite.content.directive.schema(IContact)
@zope.interface.implementer(IContact)
class Contact(uvcsite.content.components.Content):
    grok.name(u'Kontakt')
