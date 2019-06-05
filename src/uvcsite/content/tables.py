import grok
import uvcsite
import zope.interface
import zope.container.interfaces

from uvcsite import uvcsiteMF as _
from megrok.z3ctable import (
    table, Column, GetAttrColumn, CheckBoxColumn, LinkColumn)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from zope.traversing.browser import absoluteURL


class IContainerTable(zope.interface.Interface):
    pass
    

class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.context(zope.container.interfaces.IContainer)
    table(IContainerTable)

    weight = 0
    cssClasses = {'th': 'checkBox'}
    header = u""

    def renderCell(self, item):
        state = IWorkflowState(item).getState()
        if state is not None:
            state = titleForState(state)
        if state == "Entwurf":
            return CheckBoxColumn.renderCell(self, item)
        return ''


class Link(LinkColumn):
    grok.name('link')
    grok.context(zope.container.interfaces.IContainer)
    weight = 1
    table(IContainerTable)
    header = _(u"Titel")
    linkName = u"edit"

    def getLinkURL(self, item):
        """Setup link url."""
        state = IWorkflowState(item).getState()
        if state is not None:
            state = titleForState(state)
        if self.linkName is not None and state == "Entwurf":
            return '%s/%s' % (absoluteURL(item, self.request), self.linkName)
        return absoluteURL(item, self.request)

    def getLinkContent(self, item):
        return item.title

    def getSortKey(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.context(zope.container.interfaces.IContainer)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2
    table(IContainerTable)


class CreatorColumn(Column):
    grok.name('creator')
    grok.context(zope.container.interfaces.IContainer)
    header = _(u"Autor")
    weight = 99
    table(IContainerTable)

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(Column):
    grok.name('modified')
    grok.context(zope.container.interfaces.IContainer)
    header = _(u"Datum")
    weight = 100
    table(IContainerTable)

    def getSortKey(self, item):
        return item.modtime

    def renderCell(self, item):
        return uvcsite.fmtDateTime(item.modtime)


class StateColumn(GetAttrColumn):
    grok.name('state')
    grok.context(zope.container.interfaces.IContainer)
    header = _(u'Status')
    attrName = 'status'
    weight = 3
    table(IContainerTable)

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state is not None:
            return titleForState(state)
        return self.defaultValue
