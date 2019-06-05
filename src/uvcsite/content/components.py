# -*- coding: utf-8 -*-

import grok
from grokcore.component import directive
from uvcsite.content.directive import contenttype
from uvcsite.content.interfaces import (
    IContent, IProductFolder, IFolderColumnTable)
from uvcsite.utils.shorties import getPrincipal
from zope.container.interfaces import INameChooser
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer
from zope.pluggableauth.factories import Principal


@implementer(IProductFolder, IFolderColumnTable)
class ProductFolder(grok.Container):

    @property
    def name(self):
        return directive.name.bind().get(self)

    @property
    def title(self):
        return directive.title.bind().get(self)

    @property
    def description(self):
        return directive.description.bind().get(self)

    def getContentType(self):
        return contenttype.bind().get(self)

    def getContentName(self):
        return self.getContentType().__content_type__

    def add(self, content):
        name = INameChooser(self).chooseName(content.__name__ or '', content)
        self[name] = content

    @property
    def excludeFromNav(self):
        return False


@implementer(IContent)
class Content(grok.Model):
    grok.baseclass()

    schema = tuple()
    
    @property
    def meta_type(self):
        return self.__class__.__name__

    @property
    def principal(self):
        dc = IZopeDublinCore(self)
        if len(dc.creators) > 0:
            pid = dc.creators[0]
            return Principal(pid, pid)
        return getPrincipal()

    @property
    def modtime(self):
        dc = IZopeDublinCore(self)
        return dc.modified
