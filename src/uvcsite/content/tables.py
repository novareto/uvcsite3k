# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvcsite import uvcsiteMF as _
from megrok.z3ctable import (
    table, Column, GetAttrColumn, CheckBoxColumn, LinkColumn)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IFolderColumnTable, IFolderListingTable
from zope.traversing.browser import absoluteURL


class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.context(IFolderColumnTable)
    table(IFolderListingTable)
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
    grok.context(IFolderColumnTable)
    weight = 1
    table(IFolderListingTable)
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
    grok.context(IFolderColumnTable)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2
    table(IFolderListingTable)


class CreatorColumn(Column):
    grok.name('creator')
    grok.context(IFolderColumnTable)
    header = _(u"Autor")
    weight = 99
    table(IFolderListingTable)

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(Column):
    grok.name('modified')
    grok.context(IFolderColumnTable)
    header = _(u"Datum")
    weight = 100
    table(IFolderListingTable)

    def getSortKey(self, item):
        return item.modtime

    def renderCell(self, item):
        return uvcsite.fmtDateTime(item.modtime)


class StateColumn(GetAttrColumn):
    grok.name('state')
    grok.context(IFolderColumnTable)
    header = _(u'Status')
    attrName = 'status'
    weight = 3
    table(IFolderListingTable)

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state is not None:
            return titleForState(state)
        return self.defaultValue
