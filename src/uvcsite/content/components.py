import grok
import uvcsite.content.interfaces
import uvcsite.workflow
import uvcsite.content.fields

from grokcore.component import directive
from uvcsite.content.directive import contenttype
from uvcsite.utils.shorties import getPrincipal
from zope.container.interfaces import INameChooser
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer
from zope.pluggableauth.factories import Principal


@implementer(uvcsite.content.interfaces.IProductFolder)
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


@implementer(uvcsite.content.interfaces.IContent)
class Content(grok.Model):
    grok.baseclass()

    state = uvcsite.workflow.State()
    schema = tuple()

    def __init__(self, **kwargs):
        super().__init__()
        if self.schema:
            ifields = uvcsite.content.fields.Fields(*self.schema)
            for key, value in kwargs.items():
                ifield = ifields.get(key)
                if ifield is None:
                    continue
                field = ifield.bind(inst)
                field.validate(value)
                field.set(inst, value)

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
