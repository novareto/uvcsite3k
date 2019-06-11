"""
ProductFolder
=============

The Good Way
------------

First start with makeing an instance of the Container/Folder

  >>> adressbook = AdressBook()
  >>> adressbook 
  <uvcsite.tests.content.container.AdressBook object at ...>

We should now get properties for name, title and description

name

  >>> adressbook.name
  'adressbook'

title

  >>> adressbook.title
  'Adressbuch'

description

  >>> adressbook.description
  'Adressbuch ...'

And we should get back our class with the get ContentType method

  >>> adressbook.getContentType()
  <class 'uvcsite.tests.content.container.Contact'>


The not so Good Way
-------------------

   >>> class UnfallanzeigeContainer1(uvcsite.content.components.ProductFolder):
   ...     uvcsite.content.directive.contenttype(Contact)

   >>> uc = UnfallanzeigeContainer1()

We don't give a name, title and description

   >>> uc.name
   ''

   >>> uc.title

   >>> uc.description

"""
import grok
import zope.schema
import zope.interface
import zope.component
import zope.security

import uvcsite.content.components
import uvcsite.content.directive
import uvcsite.content.interfaces


class IAdressBook(uvcsite.content.interfaces.IProductFolder):
    """ Marker Interface """


class Contact(uvcsite.content.components.Content):
    grok.name(u'Kontakt')


@zope.interface.implementer(IAdressBook)
class AdressBook(uvcsite.content.components.ProductFolder):
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.content.directive.contenttype(Contact)
