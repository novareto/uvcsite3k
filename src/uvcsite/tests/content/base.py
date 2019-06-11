"""
    >>> from grokcore.component.testing import grok
    >>> grok('uvcsite.tests.fixtures.usermanagement')
    >>> grok(__name__)

    Do a unit doctest test on the base.py
    =====================================

    Let's first create an Object which inherits from Content:


    >>> import zope.security
    >>> import grok
    >>> from uvcsite.content.interfaces import IContent
    >>> from zope.publisher.browser import TestRequest
    >>> from zope.pluggableauth.factories import Principal

    >>> principal = Principal('0101010001')
    >>> request = TestRequest()

    >>> request.setPrincipal(principal)
    >>> zope.security.management.newInteraction(request)

    Does Person implement the IContentType Interface?

    >>> IContent.implementedBy(Person)
    True

    Now create an instance of Person and look for the
    behaviour.

    >>> klaus = Person()
    >>> IContent.providedBy(klaus)
    True

    >>> print(klaus.meta_type)
    Person


    Principal who created the object.

    >>> klaus.principal
    Principal('0101010001')

    >>> from zope.lifecycleevent import ObjectCreatedEvent
    >>> grok.notify(ObjectCreatedEvent(klaus))

    ModificationTime

    >>> import datetime
    >>> isinstance(klaus.modtime, datetime.datetime)
    True

    >>> zope.security.management.endInteraction()
"""

from grokcore.component import name
from uvcsite.content.components import Content


class Person(Content):
    """ Base Class For Person """

    name("Person")