import grok
import uvcsite
import uvcsite.content.interfaces
from uvcsite.content.events import AfterSaveEvent

from hurry.workflow.interfaces import IWorkflowState
from lxml import etree
from lxml.builder import E
from zope.interface import Invalid, Interface, implementer


class RestLayer(grok.IRESTLayer):
    """ Layer for Rest Access"""
    grok.restskin('api')


class ProductFolderRest(grok.REST):
    grok.layer(RestLayer)
    grok.context(uvcsite.content.interfaces.IProductFolder)
    grok.require('zope.View')

    def GET(self):
        context = self.context
        container = E('container', id=context.__name__)
        for id, obj in self.context.items():
            container.append(
                E(obj.meta_type,
                    E('id', obj.__name__),
                    E('titel', obj.title),
                    E('author', obj.principal.id),
                    E('datum', obj.modtime.strftime('%d.%m.%Y')),
                    E('status', obj.state.title))
            )
        return etree.tostring(
            container, xml_declaration=True,
            encoding='utf-8', pretty_print=True)

    def PUT(self):
        errors = []
        content = self.context.getContentType()()
        interface = content.schema[0]
        serializer = uvcsite.content.interfaces.ISerializer(content)
        serializer.work(self.body, interface, errors)

        if not errors:
            self.context.add(content)
            result = etree.Element(
                'success',
                name=content.meta_type,
                id=content.__name__
            )
            grok.notify(AfterSaveEvent(content, self.request))
        else:
            result = etree.Element('failure')
            result.extend(errors)
        return etree.tostring(result, encoding='UTF-8', pretty_print=True)


class ContentRest(grok.REST):
    grok.layer(RestLayer)
    grok.context(uvcsite.content.interfaces.IContent)
    grok.require('zope.View')

    def GET(self):
        context = self.context
        id = context.__name__
        object = etree.Element('unfallanzeige', id=id)
        schema = context.schema[0]
        element = etree.SubElement(object, context.meta_type, id=id)
        serialize_to_tree(element, schema, context)
        return etree.tostring(
            object, xml_declaration=True,
            encoding='UTF-8', pretty_print=True)


@implementer(uvcsite.content.interfaces.ISerializer)
class DefaultXMLSerializer(grok.Adapter):
    """ Default Serializer for IContent
    """
    grok.name('application/xml')
    grok.context(uvcsite.content.interfaces.IContent)

    def __call__(self):
        raise NotImplementedError('Implement your own.')
