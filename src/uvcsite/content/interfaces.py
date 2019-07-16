#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema import TextLine
from zope.interface import Interface, Attribute
from grok.interfaces import IContainer


class IUVCApplication(Interface):
    """Marker Interface the application_url method
    """


class IProductFolder(IContainer):
    """MARKER
    """


class IContent(Interface):

    state = Attribute('Workflow status.')
    schema = Attribute('Iterable of interfaces representing the schema')

    title = TextLine(
        title=u"Titel",
        description=(
            u"Bitte geben Sie einen Titel für das Dokument an. " +
            u"Dieses Dokument erscheint dann unter dem Titel in Mein Ordner."),
        required=True)


class IProductRegistration(Interface):
    """Registry for uvcsite.Content objects
    """


class ISerializer(Interface):
    """Serialization agent.
    """
    def __call__(*fields):
        """Document me
        """


class SerializationException(Exception):
    """Serialization failure report.
    """
    def __init__(self, *errors):
        self.errors = errors
